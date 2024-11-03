from __future__ import annotations

from helloworld.core import BaseEntity, Field

class DeviceEntity(BaseEntity):
    brand: str | None = Field(None, title="Brand", max_length=255)
    design_name: str | None = Field(None, title="Design Name", max_length=255)
    device_name: str | None = Field(None, title="Device Name", max_length=255)
    device_year_class: int | None = Field(None, title="Device Year Class")
    manufacturer: str | None = Field(None, title="Manufacturer", max_length=255)
    model_id: str | None = Field(None, title="Model ID", max_length=255)
    model_name: str | None = Field(None, title="Model Name", max_length=255)
    os_build_fingerprint: str | None = Field(None, title="OS Build Fingerprint", max_length=255)
    os_build_id: str | None = Field(None, title="OS Build ID", max_length=255)
    os_internal_build_id: str | None = Field(None, title="OS Internal Build ID", max_length=255)
    os_name: str | None = Field(None, title="OS Name", max_length=255)
    os_version: str | None = Field(None, title="OS Version", max_length=255)
    platform_api_level: int | None = Field(None, title="Platform API Level")
    product_name: str | None = Field(None, title="Product Name", max_length=255)
    total_memory: int | None = Field(None, title="Total Memory")

    @property
    def name(self) -> str:
        return self.design_name

