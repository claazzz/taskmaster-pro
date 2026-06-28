import sys
print("Python path:", sys.path)

try:
    from app.main import app
    print("✅ app.main импортирован!")
except ImportError as e:
    print(f"❌ Ошибка: {e}")
