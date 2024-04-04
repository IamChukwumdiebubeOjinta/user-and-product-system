from fastapi import APIRouter
# from products.product_controllers import get_products, get_product, create_product, update_product, delete_product

router = APIRouter(
    prefix="/api/v1",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/products", response_model=list[dict])