<h1>Сайт для доставки и самовывоза</h1>

<p>Сайт написан с помощью Django и используется в коммерческих целях.</p>

<h2>Стек технологий</h2>
<ul>
    <li><strong>Backend:</strong> Python, Django</li>
    <li><strong>Frontend:</strong> HTML, CSS, JavaScript</li>
    <li><strong>База данных:</strong> PostgreSQL, Redis</li>
    <li><strong>Контейнеризация:</strong> Docker</li>
    <li><strong>Тестирование:</strong> Pytest, Postman, Selenium</li>
    <li><strong>Брокер сообщений:</strong> Redis</li>
    <li><strong>Асинхронные задачи: </strong>Celery</li>
    <li><strong>Деплой: </strong>Nginx, WSGI</li>
</ul>

<h2>Планируется</h2>
<ul>
    <li><strong>Деплой:</strong> Контенеризовать проект, чтобы все микросервисы работы сглаженно на сервере</li>
    <li>Настроить Nginx и WSGI для будущего деплоя на продакшен</li>
</ul>

<h2>Что реализовано?</h2>
<ul>
    <li><strong>Backend на Django</strong>: Спроектированная микросервисзная архитектура состоящая из 5 микросервисов - <strong>Backend со статическими файлами Frontend, База данных на основе СУБД PostgreSQL, Redis как брокер сообщений и кеширование, Celery для асинхронной задачи, Бот работающий на локальной сети со своим портом с помощью Aiohttp для endpoints</strong></li>
    <li><strong>База данных</strong>: Интегрирована и настроена производительная СУБД <strong>PostgreSQL</strong> для надежного хранения данных.</li>
    <li><strong>Интеграция с Telegram-ботом</strong>: Реализовано двустороннее взаимодействие между сайтом и ботом через <strong>REST API Endpoints</strong> для автоматического обновления статусов заказов в реальном времени.</li>
    <li><strong>Платежная система</strong>: Подключено и настроено стороннее платежное <strong>API (ЮKassa)</strong> для безопасного приема онлайн-платежей.</li>
    <li><strong>Повышение производительности</strong>: Внедрено кеширование данных с помощью <strong>Redis</strong>, что позволило <strong>снизить нагрузку на сервер и ускорить загрузку ключевых страниц в 2 раза (результат подтвержден замерми через Django Debug Toolbar)</strong>.</li>
    <li><ul>
        <li><strong>Backend</strong>: Написаны модульные тесты с использованием <strong>PyTest</strong> для проверки логики приложения и работы с базой данных.</li>
        <li><strong>Frontend</strong>: Автоматизированное тестирование пользовательского интерфейса с помощью <strong>Selenium + PyTest</strong>.</li>
        <li><strong>Запросы</strong>: Протестировал через Postman</li>
    </ul></li>
    <li><strong>Telegram-бот</strong>: Разработан асинхронный бот на <strong>Aiogram</strong>, работающий на <strong>aiohttp</strong>, что позволяет ему эффективно обрабатывать входящие запросы и взаимодействовать с API сайта.</li>
    <li><strong>Инфраструктура</strong>: Настроен <strong>Nginx</strong> в качестве обратного прокси для статики и подготовки к промышленному развертыванию (deploy).</li>
</ul>
<h2>Основные функции</h2>
<ul>
    <li>📦 Обработка заказов (доставка и самовывоз)</li>
    <li>💾 Хранение заказов и данных пользователей</li>
    <li>🔐 Регистрация и авторизация пользователей</li>
    <li>🛒 Корзина покупок</li>
    <li>📱 Адаптивный интерфейс для мобильных устройств</li>
</ul>

<h2>Установка и запуск</h2>
<ol>
    <li>Клонировать репозиторий</li>
    <li>Установить зависимости: <code>pip install -r requirements.txt</code></li>
    <li>Настроить переменные окружения в <code>.env</code></li>
    <li>Запустить миграции: <code>python manage.py migrate</code></li>
    <li>Запустить сервер: <code>python manage.py runserver</code></li>
</ol>

<h2>Лицензия</h2>
<p>Коммерческое использование. Все права защищены.</p>
