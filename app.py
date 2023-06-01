from fastapi import FastAPI
from pydantic import BaseModel
from utils import *

app = FastAPI(
    title="testAPI",
    description="Test API for evaluation",
    version="1.0",
    openapi_url="/testapi/openapi.json",
    docs_url="/testapi/docs",
    redoc_url="/testapi/redoc",
)


class Product(BaseModel):
    """
    Product can be:
        1) listed (GET)
        2) added (POST)
        3) updated (PUT)
        4) deleted (DELETE)
    """
    id: int
    name: str
    description: str
    price: float


class Order(BaseModel):
    """
    Order can be:
        1) placed (POST)
        2) updated (PUT)

    > status can be retrieved (GET)
    """
    id: int
    products: list[Product]
    customer_name: str
    address: str
    total_amount: float
    order_status: str


products = intialise_random_products(Product=Product)

orders = intialise_random_orders(Order=Order, Product=Product)


@app.get("/testapi/products", status_code=status.HTTP_200_OK)
async def get_products():
    """Lists all the products in the catalogue

    Returns:
        products(list[Products]): Products in catalogue
    """
    return check_products_available(products)


@app.get("/testapi/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int):
    check_item_exist(item_id=product_id, item_list=products, item_type='Product')
    for product in products:
        if product.id == product_id:
            return product


@app.post("/testapi/product/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_product(product_id: int, product_name: str, product_description: str, product_price: float):
    """Adds a product in the catalogue

    Args:
        product_id (int): id of product
        product_name (str): name of product
        product_description (str): description of product
        product_price (float): price of product

    Returns:
        new_product (Product): the new producted added in the catalogue
    """
    new_product = Product(id=usable_id(abc_list=products, abc_id=product_id, abc_type='Product'),
                          name=product_name,
                          description=product_description,
                          price=check_product_price(product_price))
    products.append(new_product)
    return new_product


@app.put("/testapi/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_name: str = None, product_description: str = None,
                         product_price: int = None):
    """Updates any field (name, description, price) of an existing product

    Args:
        product_id (int): id of product
        product_name (str): name of product
        product_description (str): description of product
        product_price (float): price of product

    Returns:
        product (Product): updated product
    """
    check_item_exist(item_list=products, item_id=product_id, item_type='Product')
    for product in products:
        if product_id == product.id:
            if product_name is not None:
                product.name = product_name
            if product_description is not None:
                product.description = product_description
            if product_price is not None:
                product.price = check_product_price(product_price)
            return product


@app.delete("/testapi/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int):
    """Delete product in catalogue

    Args:
        product_id (int): id of the product

    Returns:
        products (list[Product]): products in catalogue
    """
    check_item_exist(item_list=products, item_id=product_id, item_type='Product')
    for product in products:
        if product_id == product.id:
            products.remove(product)
            return products


@app.post("/testapi/orders/{order_id}", status_code=status.HTTP_201_CREATED)
async def add_order(order_id: int, customer_name: str, address: str, total_amount: float, order_status: str,
                    product_ids: list[int]):
    """Add an order in the catalogue

    Args:
        order_id (int): id of order
        customer_name (str): name of customer
        address (str): address of customer
        total_amount (float): total amount of order
        order_status (str): status of order (received, shipped, delivered)
        product_ids (list[int]): list of product ids

    Returns:
        new_order (Order): New order
    """
    ordered_products = []
    real_amount = 0
    for product_id in product_ids:
        check_item_exist(item_list=products, item_id=product_id, item_type='Product')
        for product in products:
            if product.id == product_id:
                ordered_products.append(product)
                real_amount += product.price
    new_order = Order(
        id=usable_id(abc_list=orders, abc_id=order_id, abc_type='Order'),
        products=ordered_products,
        customer_name=customer_name,
        address=address,
        total_amount=check_order_amount(order_amount=total_amount, real_amount=real_amount),
        order_status=check_order_status(order_status=order_status)
    )
    orders.append(new_order)
    return new_order


@app.put("/testapi/orders/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, customer_name: str = None, address: str = None,
                       total_amount: float = None, order_status: str = None):
    """Update an existing order

    Args:
        order_id (int): id of order
        customer_name (str): name of customer
        address (str): address of customer
        total_amount (float): total amount of order
        order_status (str): status of order (received, shipped, delivered)

    Returns:
        order (Order): updated order
    """
    check_item_exist(item_id=order_id, item_list=orders, item_type='Order')
    for order in orders:
        if order_id == order.id:
            if customer_name is not None:
                order.name = customer_name
            if address is not None:
                order.address = address
            if total_amount is not None:
                order.total_amount = total_amount
            if order_status is not None and check_order_status(order_status):
                order.order_status = order_status.lower()
            return order


@app.get("/testapi/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int):
    """Get the status of an order
    Args:
        order_id (int): id of order

    Returns:
        order_status (str): status of order
    """
    check_item_exist(item_id=order_id, item_list=orders, item_type='Order')
    for order in orders:
        if order_id == order.id:
            return order.order_status
