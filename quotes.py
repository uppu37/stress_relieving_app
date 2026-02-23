import random

positive_quotes = [
    "Every day is a fresh start.",
    "You are stronger than you think.",
    "Take a deep breath and start again.",
    "Small steps every day.",
    "Peace begins with a smile."
]

stress_quotes = [
    "This too shall pass.",
    "You are not alone.",
    "It’s okay to take a break.",
    "Relax your mind and breathe slowly.",
    "One thing at a time."
]

def get_quote(mood):
    if mood == "Happy or Calm":
        return random.choice(positive_quotes)
    else:
        return random.choice(stress_quotes)