# Project Instructions (Read First)

You are working on a structured software engineering project.

## Project type
- Modular local web application for teaching software testing
- Domain: e-commerce system
- Users: vocational school students (age 15–16)

## Primary goal
- Build a realistic application that contains intentional hidden bugs
- Students will TEST the application, not fix it
- The system must remain realistic and production-like

## Core constraints
- Use Python + Flask
- Use SQLite (no ORM, raw SQL only)
- Use server-rendered templates (no frontend frameworks)
- Keep UI semi-realistic using Bootstrap + minimal JS

## Architecture rules (STRICT)
- Modular structure
- Each module must contain:
  - routes.py → HTTP layer
  - service.py → business logic
  - repository.py → DB access
- Do not mix responsibilities between layers

## Code rules (STRICT)
- Keep files under 150 lines
- Keep functions small and readable
- Avoid advanced patterns or abstractions
- Code must be understandable by beginners

## Database rules
- Use simple schema
- No complex constraints
- SQL must be readable and explicit

## Bug system rules
- The application will contain intentional bugs
- Bugs must be:
  - realistic
  - not obvious from code comments
  - not breaking the entire system
- Bugs must be controlled via a config system (later phase)

## DO NOT
- Refactor unrelated modules
- Introduce new frameworks
- Over-engineer solutions
- Add complexity not required by the task

## Development approach
- Work incrementally
- Only implement what is requested in each prompt
- Preserve existing structure and conventions

## Output expectations
- Follow exact file structure
- Do not generate unnecessary files
- Do not modify files outside requested scope

## If requirements are unclear
- Make the simplest reasonable assumption
- Do not expand scope

You are not building a demo.
You are building a controlled training environment for QA education.

