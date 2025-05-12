from google import genai
from google.genai import types

from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

MODEL = "gemini-2.0-flash"


class SupermarketItem(BaseModel):
    item_name: str = Field(description="The product")
    item_cost: float = Field(description="The price of the product")

class SupermarketInvoice(BaseModel):
    items: list[SupermarketItem] = Field(description="The list of items")
    date: str = Field(description="The date of the invoice")
    total_cost: float = Field(description="The total cost of the invoice")


def analyze_pdf(data_bytes):
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            "Extract the structured data from the following PDF file",
            types.Part.from_bytes(
                data=data_bytes,
                mime_type='application/pdf',
            ),
        ],
        config={'response_mime_type': 'application/json',
                'response_schema': SupermarketInvoice
        }
    )
    
    return response.parsed.model_dump()


def analyze_unhealthy_items(invoice_data):
    response = client.models.generate_content(
        model=MODEL,
        contents=f"Which items are unhealthy?\n{invoice_data}",
    )
    
    return response.text


def suggest_recipes(invoice_data):
    response = client.models.generate_content(
        model=MODEL,
        contents=f"Suggest a few recipes based on those items:\n{invoice_data}",
    )
    
    return response.text
