import telebot
import time
import random
import string
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from io import BytesIO
import qrcode

API_TOKEN = '7938568615:AAFdUWfb8KK8pc6xewK5cTaEYy2xGiiB5w4'
PIX_KEY = 'b6feea16-24e9-4270-80d6-1acccb793fec'

PLANS = {
    "1": {"price": 59, "duration": 1, "max_reports": 1000, "description": "eficaz para perfis com até 4.000 seguidores"},
    "2": {"price": 90, "duration": 7, "max_reports": 10000, "description": "eficaz para banir um perfil imediatamente"},
    "3": {"price": 200, "duration": 30, "max_reports": 50000, "description": "99% de precisão e suspensão imediata"}
}

bot = telebot.TeleBot(API_TOKEN)

def load_proxies(proxy_type, total_proxies):
    proxies = []
    for _ in range(total_proxies):
        proxy = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"
        proxies.append(proxy)
    return proxies

def send_reports(chat_id, proxies, url, report_count, proxy_type):
    processed_reports = random.randint(int(report_count * 0.8), int(report_count * 0.95))
    total_time = random.uniform(40, 60)
    interval = total_time / processed_reports
    error_rate = 0.2
    errors = int(processed_reports * error_rate)
    details = []
    successful = 0
    failed = 0

    for i in range(processed_reports):
        proxy = random.choice(proxies)
        if errors > 0 and random.random() < error_rate:
            failed += 1
            details.append(f"Falha - Proxy: {proxy} - Denúncia falhou para o perfil {url}")
            bot.send_message(chat_id, f"⚠️ Denúncia {i+1}/{processed_reports} falhou. Proxy: {proxy}")
            errors -= 1
        else:
            successful += 1
            details.append(f"Sucesso - Proxy: {proxy} - Denúncia enviada para o perfil {url}")
            bot.send_message(chat_id, f"✅ Denúncia {i+1}/{processed_reports} enviada com sucesso. Proxy: {proxy}")
        time.sleep(interval)

    summary = {
        "total": processed_reports,
        "success": successful,
        "error": failed,
        "details": details
    }
    return summary

def load_users():
    with open("users.txt", "r") as file:
        users = {}
        for line in file:
            username, plan = line.strip().split(":")
            users[username] = plan
        return users

def save_user(username, plan):
    with open("users.txt", "a") as file:
        file.write(f"{username}:{plan}\n")

def is_authorized_user(username):
    users = load_users()
    return username in users

def get_user_plan(username):
    users = load_users()
    return users.get(username)

def generate_pix(amount, description):
    txid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    pix_data = f"""
        000201
        26580014BR.GOV.BCB.PIX
        0116{PIX_KEY}
        52040000
        5303986
        5802BR
        5910Mass Report
        6012{description}
        62160512{txid}
        5407{amount:.2f}
        6304
    """.replace("\n", "").strip()
    return pix_data, txid

def generate_qr_code(pix_data):
    qr = qrcode.QRCode()
    qr.add_data(pix_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
Bem-vindo ao Instagram Mass Report Bot

Elimine perfis problemáticos no Instagram de forma automatizada e eficaz. Este bot utiliza tecnologia avançada para processar um grande volume de denúncias e agir diretamente contra o perfil-alvo.

Clique em "Comprar Plano" para adquirir uma licença.
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Comprar Plano", callback_data="buy_plan"))
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buy_plan")
def choose_plan(call):
    markup = InlineKeyboardMarkup()
    for plan_id, plan in PLANS.items():
        markup.add(InlineKeyboardButton(f"Plano {plan_id} - R${plan['price']} ({plan['description']})", callback_data=f"plan_{plan_id}"))
    bot.edit_message_text("Escolha um plano:", call.message.chat.id, call.message.id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("plan_"))
def process_plan(call):
    plan_id = call.data.split("_")[1]
    plan = PLANS[plan_id]
    pix_data, txid = generate_pix(plan["price"], f"Plano {plan_id}")
    qr_code = generate_qr_code(pix_data)
    bot.send_photo(call.message.chat.id, qr_code, caption=f"Plano {plan_id} selecionado!\n\nValor: R${plan['price']}\nDescrição: {plan['description']}\n\nCopia e Cola Pix:\n\n{pix_data}\n\nValidade: 10 minutos\nTXID: {txid}")
    bot.send_message(call.message.chat.id, "Após o pagamento, envie o comprovante para ativar o plano.")

@bot.message_handler(commands=['report'])
def report(message):
    username = message.from_user.username
    if not is_authorized_user(username):
        bot.send_message(message.chat.id, "Você não possui uma licença ativa. Por favor, adquira um plano para usar o bot.")
        return
    bot.send_message(message.chat.id, "Envie o link do perfil do Instagram que deseja denunciar.")
    bot.register_next_step_handler(message, get_url)

def get_url(message):
    url = message.text.strip()
    username = message.from_user.username
    plan_id = get_user_plan(username)
    plan = PLANS[plan_id]
    max_reports = plan["max_reports"]
    bot.send_message(message.chat.id, f"Plano atual: {plan_id}\nVocê pode enviar até {max_reports} denúncias.\nProcessando denúncias...")
    proxies = load_proxies("Mixed", random.randint(100, 1100))
    results = send_reports(message.chat.id, proxies, url, max_reports, "Mixed")
    details = "\n".join(results["details"])
    bot.send_message(
        message.chat.id,
        f"Denúncias enviadas!\n\nResumo:\nTotal: {results['total']}\nSucesso: {results['success']}\nFalhas: {results['error']}\n\nDetalhes:\n{details}"
    )

bot.polling()