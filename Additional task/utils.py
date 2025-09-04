import os
import requests
from dotenv import load_dotenv
from groq import Groq

# -------------------------
# Load API Key from .env
# -------------------------
load_dotenv()

# -------------------------
# Custom Image Prompts for Each State
# -------------------------
IMAGE_PROMPTS = {
    "Andhra Pradesh": {
        "Culture": "Traditional Kuchipudi dance performance in Andhra Pradesh with dancers in costume",
        "Dressing Style": "Women in bright sarees and men in white dhoti typical of Andhra Pradesh",
        "Famous Food": "Authentic Andhra thali with spicy curries, gongura pachadi, and biryani",
        "Places to Explore": "Tirupati Balaji Temple with pilgrims",
        "Language": "People reading Telugu script on walls or books"
    },
    "Arunachal Pradesh": {
        "Culture": "Tribal festival celebration in Arunachal Pradesh with traditional dance",
        "Dressing Style": "Tribal men and women in colorful traditional attire with headgear",
        "Famous Food": "Plate of Thukpa and Momos typical of Arunachal cuisine",
        "Places to Explore": "Tawang Monastery surrounded by mountains",
        "Language": "People reading and writing in Assamese and tribal scripts"
    },
    "Assam": {
        "Culture": "Bihu dance performance in Assam with traditional dhol",
        "Dressing Style": "Women in Mekhela Chador and men in dhoti with gamocha",
        "Famous Food": "Assamese thali with rice, fish curry, and tenga",
        "Places to Explore": "Kaziranga National Park with rhinoceros",
        "Language": "People reading Assamese script on books"
    },
    "Bihar": {
        "Culture": "Chhath Puja rituals on river banks in Bihar",
        "Dressing Style": "Women in vibrant sarees and men in dhoti kurta typical of Bihar",
        "Famous Food": "Traditional Bihar thali with Litti Chokha",
        "Places to Explore": "Mahabodhi Temple at Bodh Gaya",
        "Language": "People reading and writing in Hindi and Maithili scripts"
    },
    "Chhattisgarh": {
        "Culture": "Folk dancers performing Panthi dance in Chhattisgarh",
        "Dressing Style": "Tribal attire with ornaments and bright fabrics",
        "Famous Food": "Chhattisgarhi plate with Chana Samosa and Fara",
        "Places to Explore": "Chitrakoot Waterfalls in Bastar",
        "Language": "People reading Chhattisgarhi and Hindi scripts"
    },
    "Goa": {
        "Culture": "Carnival parade in Goa with colorful costumes and floats",
        "Dressing Style": "People in modern casuals with traditional Portuguese influence",
        "Famous Food": "Goan fish curry with rice and seafood platter",
        "Places to Explore": "Beaches of Goa with palm trees and sunset",
        "Language": "People speaking Konkani script near churches"
    },
    "Gujarat": {
        "Culture": "Garba dance celebration during Navratri in Gujarat",
        "Dressing Style": "Women in colorful Ghagra Choli and men in Kediyu",
        "Famous Food": "Gujarati thali with dhokla, thepla, and farsan",
        "Places to Explore": "Somnath Temple on the coast",
        "Language": "Gujarati script on walls and books"
    },
    "Haryana": {
        "Culture": "Haryanvi folk dancers performing on stage",
        "Dressing Style": "Men in dhoti kurta and turban, women in ghagra and dupatta",
        "Famous Food": "Traditional Haryana meal with Bajra roti and butter milk",
        "Places to Explore": "Kurukshetra battlefield memorial",
        "Language": "People conversing in Hindi and Haryanvi dialect"
    },
    "Himachal Pradesh": {
        "Culture": "Kullu Dussehra festival with processions",
        "Dressing Style": "Men and women in warm woolen Himachali caps and shawls",
        "Famous Food": "Dham meal served on leaves",
        "Places to Explore": "Snow covered mountains of Manali",
        "Language": "People reading Hindi and Pahadi script"
    },
    "Jharkhand": {
        "Culture": "Tribal festival Sarhul celebration in Jharkhand",
        "Dressing Style": "Tribal attire with red and white costumes",
        "Famous Food": "Jharkhand thali with Thekua and Dhuska",
        "Places to Explore": "Dassam Falls near Ranchi",
        "Language": "People speaking and reading in Hindi and tribal scripts"
    },
    "Karnataka": {
        "Culture": "Yakshagana dance drama performance in Karnataka",
        "Dressing Style": "Women in traditional Mysore silk sarees, men in panche",
        "Famous Food": "Karnataka thali with Bisi Bele Bath and Mysore Pak",
        "Places to Explore": "Mysore Palace illuminated at night",
        "Language": "Kannada script on boards and books"
    },
    "Kerala": {
        "Culture": "Kathakali dance with full costume and makeup",
        "Dressing Style": "Women in Kerala kasavu saree, men in mundu",
        "Famous Food": "Kerala Sadya meal served on banana leaf",
        "Places to Explore": "Backwaters of Alleppey with houseboats",
        "Language": "Malayalam script on signboards"
    },
    "Madhya Pradesh": {
        "Culture": "Folk dance performance during Khajuraho festival",
        "Dressing Style": "Traditional tribal dresses with jewelry",
        "Famous Food": "Poha Jalebi and Dal Bafla from Madhya Pradesh",
        "Places to Explore": "Khajuraho Temples with carvings",
        "Language": "Hindi script and tribal dialects"
    },
    "Maharashtra": {
        "Culture": "Lavani dance performance with women in nauvari saree",
        "Dressing Style": "Men in dhoti kurta with pheta, women in saree",
        "Famous Food": "Maharashtrian thali with Puran Poli and Misal Pav",
        "Places to Explore": "Gateway of India in Mumbai",
        "Language": "Marathi script on walls and signboards"
    },
    "Manipur": {
        "Culture": "Ras Leela dance performance in Manipur",
        "Dressing Style": "Women in Phanek skirt, men in dhoti kurta",
        "Famous Food": "Manipuri thali with Eromba and fish curry",
        "Places to Explore": "Loktak Lake with floating islands",
        "Language": "Manipuri (Meitei) script on boards"
    },
    "Meghalaya": {
        "Culture": "Shad Suk Mynsiem dance festival in Meghalaya",
        "Dressing Style": "Khasi women in Jainsem dress, men in traditional attire",
        "Famous Food": "Jadoh rice dish with meat",
        "Places to Explore": "Living root bridges of Meghalaya",
        "Language": "Khasi script and English signs"
    },
    "Mizoram": {
        "Culture": "Cheraw bamboo dance performed by Mizoram tribes",
        "Dressing Style": "Traditional Mizo attire with striped dress",
        "Famous Food": "Mizo meal with Bai and rice",
        "Places to Explore": "Blue Mountain (Phawngpui) in Mizoram",
        "Language": "Mizo script and English writing"
    },
    "Nagaland": {
        "Culture": "Hornbill festival with tribal dances",
        "Dressing Style": "Tribal men and women in colorful shawls and ornaments",
        "Famous Food": "Naga thali with smoked pork and rice",
        "Places to Explore": "Dzukou Valley with flowers",
        "Language": "Naga dialects and English writing"
    },
    "Odisha": {
        "Culture": "Odissi classical dance performance in Odisha",
        "Dressing Style": "Women in Sambalpuri saree, men in dhoti",
        "Famous Food": "Odisha thali with Dalma and Pakhala Bhata",
        "Places to Explore": "Konark Sun Temple with carvings",
        "Language": "Odia script on walls and books"
    },
    "Punjab": {
        "Culture": "Group of men performing energetic Bhangra dance in colorful turbans",
        "Dressing Style": "Punjabi man in kurta-pajama and turban, woman in vibrant salwar suit",
        "Famous Food": "Punjabi thali with butter chicken, naan, and a glass of lassi",
        "Places to Explore": "Golden Temple in Amritsar at sunset",
        "Language": "Punjabi script on a book with people conversing"
    },
    "Rajasthan": {
        "Culture": "Kalbelia folk dance in Rajasthan with women in swirling skirts",
        "Dressing Style": "Men in colorful turbans, women in lehenga choli",
        "Famous Food": "Rajasthani thali with Dal Baati Churma and Gatte ki sabzi",
        "Places to Explore": "Hawa Mahal in Jaipur",
        "Language": "Rajasthani and Hindi script on walls"
    },
    "Sikkim": {
        "Culture": "Monks performing ritual dance in Sikkim monastery",
        "Dressing Style": "People in Buddhist influenced attire",
        "Famous Food": "Sikkimese thali with Momos and Thukpa",
        "Places to Explore": "Kanchenjunga mountains from Sikkim",
        "Language": "Sikkimese and Nepali scripts"
    },
    "Tamil Nadu": {
        "Culture": "Bharatanatyam classical dance performance in Tamil Nadu",
        "Dressing Style": "Women in Kanchipuram silk sarees, men in veshti",
        "Famous Food": "Tamil Nadu thali with dosa, idli, sambar, and filter coffee",
        "Places to Explore": "Meenakshi Temple in Madurai",
        "Language": "Tamil script on books and signboards"
    },
    "Telangana": {
        "Culture": "Perini dance performance from Telangana",
        "Dressing Style": "Women in bright sarees, men in white dhoti typical of Telangana",
        "Famous Food": "Hyderabadi biryani and Mirchi ka Salan",
        "Places to Explore": "Charminar in Hyderabad",
        "Language": "Telugu script on books and walls"
    },
    "Tripura": {
        "Culture": "Garia dance festival of Tripura tribes",
        "Dressing Style": "Tribal attire with traditional ornaments",
        "Famous Food": "Tripuri meal with Mui Borok and rice",
        "Places to Explore": "Ujjayanta Palace in Agartala",
        "Language": "Bengali and Kokborok scripts"
    },
    "Uttar Pradesh": {
        "Culture": "Kathak dance performance in Uttar Pradesh",
        "Dressing Style": "Women in sarees, men in kurta pajama",
        "Famous Food": "Awadhi thali with kebabs and biryani",
        "Places to Explore": "Taj Mahal in Agra",
        "Language": "Hindi and Urdu script on books and walls"
    },
    "Uttarakhand": {
        "Culture": "Kumaoni folk dance performance in Uttarakhand",
        "Dressing Style": "People in woolen traditional attire with caps",
        "Famous Food": "Uttarakhand thali with Kafuli and Aloo ke Gutke",
        "Places to Explore": "Kedarnath Temple in the Himalayas",
        "Language": "Hindi and Garhwali script on books"
    },
    "West Bengal": {
        "Culture": "Durga Puja celebration in West Bengal with idols",
        "Dressing Style": "Women in red and white sarees, men in dhoti kurta",
        "Famous Food": "Bengali thali with fish curry, rice, and rasgulla",
        "Places to Explore": "Howrah Bridge in Kolkata",
        "Language": "Bengali script on signboards and books"
    }
}


# -------------------------
# Pollinations API (for images)
# -------------------------
def get_pollinations_image(prompt: str) -> str:
    """
    Generate image URL from Pollinations API based on a given prompt.
    """
    safe_prompt = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{safe_prompt}"


# -------------------------
# Groq API (for text generation)
# -------------------------
def get_groq_client():
    """
    Initialize Groq client with API key from environment.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GROQ_API_KEY. Please set it in your .env file.")
    return Groq(api_key=api_key)


def get_groq_content(prompt: str) -> str:
    """
    Get text content from Groq API for a given prompt.
    """
    client = get_groq_client()
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides short, neat, factual information."},
            {"role": "user", "content": prompt},
        ],
    )
    return chat_completion.choices[0].message.content
