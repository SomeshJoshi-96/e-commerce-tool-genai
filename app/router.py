from rapidfuzz.distance.Levenshtein_py import similarity
from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        # Returns & exchanges
        "What’s your return and exchange policy?",
        "How do I initiate a return if I’m not satisfied?",
        "Can I return a product after 30 days?",
        "Are return shipping fees on you or me?",
        "How long do I have to send an item back?",
        "When the product will be delivered?"

        # Refund timing
        "When will I get my refund once I return something?",
        "How long does it take to process my refund?",
        "What’s the turnaround time for a refund after return?",

        # Order tracking
        "How can I track the status of my order?",
        "Where do I find my shipment tracking number?",
        "Can you tell me how to view my order’s delivery progress?",

        # Payment methods
        "What payment methods do you accept?",
        "Which cards or digital wallets are supported?",
        "Do you take UPI, net banking, or PayPal?"
        "Can I pay cash for payment?",

        # Discounts & credit-card offers
        "Are there any discounts for HDFC credit-card holders?",
        "What promotional offers come with an HDFC card?",
        "Can I get a discount when I pay with my HDFC credit card?"
        "How do you give dicounts?"
        "What is the criteria for discounts?"
    ],
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)
small_talk = Route(
    name='small_talk',
    utterances=[
        "Hey there! How’s your day going?",
        "Hi! What’s on your mind today?",
        "How are you feeling right now?",
        "What have you been up to lately?",
        "Nice to see you—how are things?",
        "Can I ask how your day has been so far?",
        "Hello! How’s everything with you?",
        "What’s new and exciting in your world?",
        "How are you doing today?",
        "Is there anything fun planned for today?"
    ]
)

routes = [faq, sql,small_talk]

router = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")

if __name__ == "__main__":
    print(router("What is the time to get a refund?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)
    print(router("Do you feel like a robot?").name)