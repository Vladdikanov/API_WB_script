from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime, timedelta
import pandas as pd
import random

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    order_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")



engine = create_engine('sqlite:///orders.db')

Base.metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(text("""
    CREATE VIEW IF NOT EXISTS daily_sales_report AS
    SELECT 
        order_date AS date,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(total_amount) AS total_sales,
        SUM(total_amount) / COUNT(DISTINCT customer_id) AS avg_check
    FROM orders
    GROUP BY order_date
    ORDER BY order_date DESC
    """))

    conn.execute(text("""
    CREATE VIEW IF NOT EXISTS top_products_last_month AS
    SELECT 
        product_id,
        SUM(quantity * unit_price) AS sales_amount
    FROM order_items
    JOIN orders ON order_items.order_id = orders.order_id
    WHERE order_date >= date('now', '-1 month')
    GROUP BY product_id
    ORDER BY sales_amount DESC
    LIMIT 3
    """))

    conn.execute(text("""
    CREATE VIEW IF NOT EXISTS avg_orders_per_customer AS
    SELECT 
        customer_id,
        CAST(COUNT(order_id) AS FLOAT) / 
            (SELECT COUNT(DISTINCT order_date) 
             FROM orders 
             WHERE order_date >= date('now', '-3 month')) AS avg_orders
    FROM orders
    WHERE order_date >= date('now', '-3 month')
    GROUP BY customer_id
    ORDER BY avg_orders DESC
    """))


def insert_test_data():
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(OrderItem).delete()
    session.query(Order).delete()

    test_orders = [
        Order(
            customer_id=random.randint(1, 3),
            order_date=datetime.now() - timedelta(days=(random.randint(0,5) - i)),
            total_amount=((1 + i) * (60 + i * 5)) + ((2 + i) * (50 + i * 4)),
            items=[
                OrderItem(product_id=101 + i, quantity=1 + i, unit_price=60 + i * 5),
                OrderItem(product_id=200 + i, quantity=2 + i, unit_price=50 + i * 4)
            ]
        ) for i in range(30)
    ]

    session.add_all(test_orders)
    session.commit()
    session.close()

insert_test_data()

def daily_sales():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM daily_sales_report", conn)
        print("Аналитический отчет по продажам за день:")
        print(df.to_string(index=False))

# daily_sales()

def top_products():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM top_products_last_month", conn)
        print("Топ-3 продукта за последний месяц:")
        print(df.to_string(index=False))

# top_products()

def avg_orders():
    with engine.connect() as conn:
        # conn.execute("SELECT * FROM avg_orders_per_customer")
        # print(conn.fetch_all())
        df = pd.read_sql("SELECT * FROM avg_orders_per_customer", conn)
        print("Среднее количество заказов на клиента (3 месяца):")
        print(df.to_string(index=False))

# avg_orders()


