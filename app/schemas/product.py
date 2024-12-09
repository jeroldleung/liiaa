from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(description="Product name in Chinese")
    serial_number: str = Field(description="Product serial number")
    wattage: str = Field(description="Product wattage")
    size: str = Field(description="Product size")
    color: str = Field(description="Product color")
