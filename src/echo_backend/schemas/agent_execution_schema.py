import re
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TranscriptMessage(BaseModel):
    role: Literal["assistant", "user"]
    content: str


class FieldValidation(BaseModel):
    pattern: str | None = None
    is_valid: bool | None = None
    expected_type: str | None = None


class ExtractedField(BaseModel):
    objective: str | None = None
    subjective: str | None = None
    confidence: float | None = None
    confidence_label: str | None = None
    validation: FieldValidation | None = None
    reasoning_objective: str | None = None
    reasoning_subjective: str | None = None


class ServiceDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    provider_time: ExtractedField | None = Field(None, alias="Service Provider Time")
    provider_date: ExtractedField | None = Field(None, alias="Service provider date")
    provider_price: ExtractedField | None = Field(None, alias="service provider price")
    provider_availability: ExtractedField | None = Field(None, alias="service provider availability")


class GeneralDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    call_summary: ExtractedField | None = Field(None, alias="Call Summary")


class ExtractedData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    service_details: ServiceDetails | None = Field(None, alias="Service details")
    general: GeneralDetails | None = Field(None, alias="General")


class AgentExecutionSchema(BaseModel):
    id: str
    agent_id: str
    status: str
    transcript: list[TranscriptMessage] = []
    summary: str | None = None
    extracted_data: ExtractedData | None = None
    recording_url: str | None = None  # flattened from telephony_data

    @model_validator(mode="before")
    @classmethod
    def flatten_recording_url(cls, data: Any):
        if isinstance(data, dict):
            data = dict(data)
            telephony = data.get("telephony_data") or {}
            data["recording_url"] = telephony.get("recording_url")
        return data

    @field_validator("transcript", mode="before")
    @classmethod
    def parse_transcript(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            pattern = re.compile(
                r"^(assistant|user):\s*(.*?)(?=^(?:assistant|user):|\Z)",
                re.M | re.S,
            )
            return [
                {"role": role, "content": content.strip()}
                for role, content in pattern.findall(v)
            ]
        return v