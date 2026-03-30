# Tend (Working Name)

#### Video Demo: https://youtu.be/urqQSYvYAzM

#### Live Application: https://tend-3b2l.onrender.com

#### Demo Environment: 

The live application is currently running as a shared demo space. This means that all users interact with the same set of zones and observations rather than having separate accounts. This approach was chosen to keep the application simple for demonstration and testing purposes.

In future iterations, the application could be extended to support user accounts and personalized spaces, but for this version the shared environment allows multiple users to explore the full functionality of the system without requiring authentication.

Tend is a web-based application designed to help users track, understand, and reflect on their garden or growing spaces. The goal of this project is to create a simple, yet intelligent, zone-based system that allows users to log observations about their environment and receive helpful insights without needing to manually analyze everything themselves.

The core idea behind Tend is that people may become overwhelmed with what is happening in their garden over time, especially new gardeners. Instead of relying on memory or complex tracking systems, Tend provides a calm and intuitive interface where users can organize their space into zones and record what they notice. Over time, the system uses these observations along with environmental context to generate reflections that help users better understand patterns and changes.

The main feature of the application is the concept of "zones." A zone represents a physical area such as a garden bed or section of land. Each zone contains observations, which are simple notes entered by the user. These observations are timestamped and stored in the database so that users can build a history of what is happening in each space.

A key feature of the system is the reflection engine. When a user clicks the reflect button, the application gathers recent observations and generates a single, focused insight. Rather than overwhelming the user with multiple suggestions, the system is intentionally designed to return one meaningful thought at a time. This keeps the experience simple and supportive.

During development, I initially explored adding automatic plant suggestions for each zone. However, I chose to remove this feature because it was not truly tied to the user’s data and risked becoming generic. Instead, I focused on generating insights based on actual observations, time, and environmental context. This decision helped keep the system grounded and aligned with real conditions.

Another important part of the project is the integration of location and weather context. The application uses this information to influence both insights and the visual experience. The interface includes a theme system that adapts based on weather and time of day, such as sunny, rainy, cloudy, or neutral conditions, as well as dawn, day, dusk, and night. This creates a more immersive experience that reflects the user’s real environment.

The application is built using Flask as the backend framework. It uses a PostgreSQL database to store zones, observations, settings, and related data. During development, I refactored the database layer to fully support Postgres, creating a more production-ready and consistent architecture.

One of the most important parts of this project was refactoring the code into a more modular structure. Initially, more logic lived in fewer files, but as the project grew, I separated responsibilities into distinct modules to improve clarity and maintainability.

The `tend/__init__.py` file uses an application factory pattern to create and configure the Flask app. This includes initializing the application, setting up configuration, and registering routes. Refactoring into an application factory helped organize startup logic and made the app easier to extend.

The `tend/routes.py` file contains all route logic for the application. This includes rendering pages, handling form submissions, creating zones, adding observations, and triggering reflections. Separating routes into their own file makes the flow of user interactions easier to understand.

The `tend/db.py` file manages database connections and queries, including handling communication with the PostgreSQL database. This abstraction keeps database logic separate from application logic and improves maintainability.

The `tend/weather_theme.py` file contains logic related to environmental context and theming. It builds theme classes based on weather and time of day, which are then injected into templates.

The `tend/page_context.py` file is responsible for injecting shared data into templates, such as theme and weather context, allowing for consistent rendering across pages.

The `tend/helpers.py` file contains utility functions used throughout the application.

The `templates/` folder contains all HTML templates used to render the user interface, including the homepage, zone views, and settings page. These templates use Jinja to display dynamic data.

The `static/` folder contains frontend assets such as CSS and JavaScript. The styling system includes dynamic classes that reflect weather and time-based themes, contributing to the overall experience.

The `schema.sql` file defines the structure of the database tables, and `plants.sql` is used to seed initial plant data.

The `requirements.txt` file lists the Python dependencies required to run the application.

One of the key design decisions in this project was to prioritize simplicity. Instead of building a complex system with many features, I focused on a small set of core interactions: zones, observations, and reflections. I also chose to present only one insight at a time to avoid overwhelming the user.

Another important decision was to treat the AI component as a supportive assistant rather than an authoritative system. The goal is to help users think more clearly and notice patterns, not to replace human judgment.

Future improvements could include plant-level profiles within zones, a planning interface for organizing garden layouts and materials, and a local-first version of the system that runs on a device such as a Raspberry Pi for offline use.

Overall, Tend is designed to be a lightweight but thoughtful tool that helps users build awareness of their space over time, combining tracking, environmental context, and reflection in a simple and intuitive way.
