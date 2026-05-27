# BlindsPro - Автоматизированная система управления заказами жалюзи

Полнофункциональная веб-система для автоматизации процесса заказа, производства и монтажа жалюзи с современным минималистичным дизайном в стиле premium SaaS-платформы.

## 🚀 Функционал

### 1. **Онлайн-конфигуратор жалюзи**
- Выбор типов жалюзи (горизонтальные, вертикальные, рулонные)
- Ввод размеров с валидацией
- Выбор материалов, цветов и текстур
- Типы управления (ручное, моторизованное, смарт)
- Дополнительные опции
- **Динамический расчет цены в реальном времени**
- Пошаговый wizard UI с preview

### 2. **CRM-модуль**
- Список и карточки клиентов
- История заказов
- Поиск и фильтрация
- Статусы взаимодействия
- Заметки менеджеров
- История коммуникаций

### 3. **Управление заказами**
- Создание и редактирование
- Статусы: новый → обработка → производство → готов → доставлен → установлен
- Таблица с фильтрацией и сортировкой
- Детальная страница заказа
- Timeline статусов

### 4. **Производственный модуль**
- Производственные задания
- Распределение заказов по цехам
- Контроль выполнения
- Загрузка производства
- Приоритеты заказов

### 5. **Складской учет**
- Материалы и комплектующие
- Остатки
- Поступления и списания
- Автоматическое резервирование
- Уведомления о низких остатках

### 6. **Планировщик работ**
- Календарь замеров и монтажей
- Назначение монтажных бригад
- Drag & drop для задач
- Расписание работ

### 7. **Админ-панель**
- Управление пользователями
- Роли: администратор, менеджер, производство, монтажник
- Настройки системы
- Логирование действий

## 🏗️ Архитектура

### Backend (FastAPI)
- **Clean Architecture** с разделением на слои
- **JWT авторизация**
- **PostgreSQL + SQLAlchemy ORM**
- **Alembic** для миграций
- **REST API**

### Frontend (Next.js + React)
- **TypeScript**
- **TailwindCSS + shadcn/ui**
- **Framer Motion** для анимаций
- **React Query** для синхронизации
- **Zustand** для состояния

## 🎨 Дизайн

- 🌞 Светлая минималистичная тема
- 💎 Premium SaaS-стиль (Linear, Stripe, Notion)
- ✨ Glassmorphism элементы
- 🎯 Responsive design
- 🔄 Smooth animations
- ♿ Accessibility first

## 📁 Структура проекта

```
blindspro/
├── backend/
│   ├── app/
│   │   ├── core/              # Безопасность, исключения
│   │   ├── db/                # Модели и схемы
│   │   ├── repositories/      # Data access layer
│   │   ├── services/          # Business logic
│   │   ├── routers/           # API endpoints
│   │   └── main.py
│   ├── migrations/            # Alembic
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/                   # Next.js маршруты
│   ├── components/            # Переиспользуемые компоненты
│   ├── lib/                   # Утилиты и hooks
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## 🛠️ Технологии

**Backend:**
- FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic

**Frontend:**
- Next.js 14+, React 18+, TypeScript, TailwindCSS, shadcn/ui, Framer Motion, React Query

## 📦 Установка и запуск

### Требования
- Docker и Docker Compose
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

### Локальная разработка

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up
```

## 📝 Лицензия

MIT

## 👤 Автор

saydullayev-d
