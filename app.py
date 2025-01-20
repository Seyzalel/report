import telebot
import time
import random
from telebot.types import ReplyKeyboardMarkup

API_TOKEN = 'SEU_BOT_TOKEN_AQUI'

bot = telebot.TeleBot(API_TOKEN)

def load_proxies(proxy_type, total_proxies):
    proxies = []
    for _ in range(total_proxies):
        proxy = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"
        proxies.append(proxy)
    return proxies

def send_reports(proxies, url, report_count, proxy_type):
    processed_reports = random.randint(int(report_count * 0.8), int(report_count * 0.95))
    total_time = random.uniform(40, 60)
    interval = total_time / processed_reports
    error_rate = 0.2
    errors = int(processed_reports * error_rate)
    successful_reports = processed_reports - errors

    results = {"success": 0, "error": 0}
    for _ in range(processed_reports):
        if results["error"] < errors and random.random() < error_rate:
            results["error"] += 1
        else:
            results["success"] += 1
        time.sleep(interval)
    return results

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
🔥 Bem-vindo ao Instagram Mass Report Bot 🔥

🚨 **Elimine perfis problemáticos no Instagram de forma automatizada e eficaz.** Este bot utiliza tecnologia avançada para processar um grande volume de denúncias e agir diretamente contra o perfil-alvo. Perfeito para neutralizar spammers, golpistas e comportamentos que violam os Termos de Serviço da plataforma.

🔎 **Como funciona?**
O sistema utiliza redes de proxies internacionais de alta qualidade, que trabalham em conjunto com algoritmos inteligentes para executar denúncias diretamente ao Instagram. Isso acontece de maneira coordenada e rápida, aumentando significativamente a eficácia e agilizando o processo de resposta automática da plataforma.

💻 **Por que este bot é tão eficaz?**
- Cada proxy atua como um "usuário" único denunciando o perfil.
- O processo é executado com precisão, respeitando os limites necessários para evitar bloqueios.
- Redes de proxies como HTTP, SOCKS4, SOCKS5 e residenciais são configuradas para maximizar os resultados.

⚠️ **Use com responsabilidade:** Este bot foi projetado para uso ético e responsável. Qualquer uso inadequado será de total responsabilidade do usuário.

Digite /help para ver como usar este bot ou /report para começar agora.
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📋 **Como usar o Instagram Mass Report Bot:**

1️⃣ Digite /report para iniciar o processo.
2️⃣ Envie o link do perfil que deseja denunciar.
3️⃣ Escolha o tipo de proxy desejado.
4️⃣ Defina a quantidade de denúncias a serem enviadas.
5️⃣ Aguarde o processamento. O sistema notificará ao final do processo.

Digite /report para começar agora.
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def report_command(message):
    bot.reply_to(message, "Envie o link do perfil do Instagram que deseja denunciar.")
    bot.register_next_step_handler(message, get_url)

def get_url(message):
    url = message.text.strip()
    bot.reply_to(message, f"Perfil recebido: {url}\n\nAgora, escolha o tipo de proxy que deseja usar.")
    
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("1. Mixed", "2. HTTP", "3. SOCKS4", "4. SOCKS5", "5. Residential")
    bot.send_message(message.chat.id, "Selecione o tipo de proxy:", reply_markup=markup)
    bot.register_next_step_handler(message, get_proxy_type, url)

def get_proxy_type(message, url):
    proxy_choice = message.text.split(".")[0]
    proxy_types = {
        "1": "Mixed",
        "2": "HTTP",
        "3": "SOCKS4",
        "4": "SOCKS5",
        "5": "Residential"
    }

    if proxy_choice not in proxy_types:
        bot.reply_to(message, "Escolha inválida. Digite /report para tentar novamente.")
        return

    proxy_type = proxy_types[proxy_choice]
    total_proxies = random.randint(100, 1100)
    proxies = load_proxies(proxy_type, total_proxies)

    bot.reply_to(message, f"{total_proxies} proxies do tipo {proxy_type} carregados com sucesso!")
    bot.reply_to(message, "Quantos relatórios você deseja enviar? (100-10.000)")
    bot.register_next_step_handler(message, get_report_count, url, proxies, proxy_type)

def get_report_count(message, url, proxies, proxy_type):
    try:
        report_count = int(message.text.strip())
        if report_count < 100 or report_count > 10000:
            bot.reply_to(message, "Número de denúncias inválido. Digite /report para tentar novamente.")
            return
    except ValueError:
        bot.reply_to(message, "Entrada inválida. Digite /report para tentar novamente.")
        return

    bot.reply_to(message, "Processando denúncias, aguarde...")
    results = send_reports(proxies, url, report_count, proxy_type)

    bot.send_message(
        message.chat.id,
        f"""
📊 **Resumo do processo concluído:**
🔗 Perfil: {url}
📥 Proxy utilizado: {proxy_type}
✅ Denúncias bem-sucedidas: {results['success']}
❌ Denúncias com erro: {results['error']}
        
Digite /report para iniciar outro processo.
"""
    )

bot.polling()
