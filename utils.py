from fastapi import HTTPException, status


def check_products_available(products):
    """Checks if there are products in the catalogue

    Args:
        products (list[Product}): list of products

    Returns:
        products (list[Product}): list of products

    Raises:
        HTTPException: 404, if there are no products in catalogue
    """
    if len(products) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products in catalogue"
        )
    return products


def check_item_exist(item_id, item_type, item_list):
    """Checks if item of any given type exist in specific list, abstract method

    Args:
        item_id (int): id of item
        item_type (str): type of item (Product/Order)
        item_list (list[Products, Orders]): list of items (Product/Order)

    Returns:
        item_id (int): id of existing item

    Raises:
        HTTPException: 404, if the item doesn't exist
    """
    for item in item_list:
        if item_id == item.id:
            return item_id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{item_type} with id: {item_id} was not found in catalogue"
    )


def usable_id(item_id, item_type, item_list):
    """Checks if specific id is already in use

    Args:
        item_id (int): id of item
        item_type (str): type of item (Product/Order)
        item_list (list[Products, Orders]): list of items (Product/Order)

    Returns:
        item_id (int): id of item (usable)

    Raises:
        HTTPException: 406, if the item id is used by another item
    """
    for item in item_list:
        if item_id == item.id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"{item_type} with id: {item_id} already exists"
            )
    return item_id


def check_product_price(price):
    """Check price of product is above a threshold

    Args:
        price (float): price of product

    Returns:
        price (float): price of product

    Raises:
         HTTPException: 406, if the price of the product is below the threshold
    """
    if price < 0.1:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Product prices must be above 0.1"
        )
    return price


def intialise_random_products(Product):
    """Initialise random products in catalogue

    Args:
        Product (BaseModel): products of type Product base model

    Returns:
        random_products (list[Product]): list of random products
    """
    random_products = [
        Product(id=1, name="TV", description="New Generation Television", price=599.99),
        Product(id=2, name="headphones", description="New Generation headphones", price=99.99),
        Product(id=3, name="laptop", description="New Generation laptop", price=1199.99)
    ]
    return random_products


def intialise_random_orders(Order, Product):
    """Initialise random orders in catalogue

    Args:
        Order (BaseModel): orders of type Order base model
        Product (BaseModel): products of type Product base model

    Returns:
        random_orders (list[Order]): list of random orders
    """
    random_orders = [
        Order(id=1,
              products=[Product(id=1, name="TV", description="New Generation Television", price=599.99)],
              customer_name="Katerina", address='Athens', total_amount='10', order_status='received'),
        Order(id=2,
              products=[
                  Product(id=1, name="TV", description="New Generation Television", price=599.99),
                  Product(id=2, name="headphones", description="New Generation headphones", price=99.99)
              ],
              customer_name="Giorgos", address='Athens', total_amount='10', order_status='received')
    ]
    return random_orders


def check_order_status(order_status):
    """Check order status is the appropriate one

    Args:
        order_status (str): status of the order (received, shipped, delivered)

    Returns:
        order_status (str): status of the order

    Raises:
        HTTPException: 406, if the order status is not received, shipped or delivered
    """
    if order_status.lower() not in ['received', 'shipped', 'delivered']:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Order status can only be: 1) received, 2) shipped, 3) delivered"
        )
    return order_status


def check_order_amount(order_amount, real_amount):
    """Checks if the total amount in the order is the same amount as in the catalogue

    Args:
        order_amount (float): total amount inserted in order
        real_amount (float): total amount calculated from the products in the order

    Returns:
        real_amount (float): total amount calculated from the products in the order

    Raises:
        HTTPException: 406, if order_amount is not equal to the real_amount
    """
    if real_amount != order_amount:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Calculated amount is: {real_amount} and order amount is: {order_amount}"
        )
    return real_amount
