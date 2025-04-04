from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os

# โหลดค่าจากไฟล์ .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# สร้าง engine เพื่อเชื่อมต่อกับฐานข้อมูล
engine = create_engine(DATABASE_URL)

# ตรวจสอบตารางที่มีอยู่ในฐานข้อมูล
inspector = inspect(engine)
tables = inspector.get_table_names()

# แสดงรายชื่อของตารางทั้งหมด
print(tables)
