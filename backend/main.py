from fastapi import FastAPI
import httpx
import asyncio
import pybreaker

app = FastAPI()

# Circuit Breaker
breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10
)

# Middleware for required header
@app.middleware("http")
async def add_student_id_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "bscs23213"
    return response


# Fake failing LLM API
async def fake_llm_call():

    # Simulate API hanging
    await asyncio.sleep(60)

    return {"response": "LLM Success"}


# Protected call
@breaker
def protected_llm_call():
    return asyncio.run(fake_llm_call())


@app.get("/ask")
async def ask_ai():

    try:
        result = protected_llm_call()
        return result

    except pybreaker.CircuitBreakerError:
        return {
            "message": "LLM service unavailable. Using fallback response."
        }

    except Exception:
        return {
            "message": "LLM timeout occurred."
        }