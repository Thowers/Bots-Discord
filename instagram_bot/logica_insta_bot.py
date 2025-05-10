import instaloader
import os
from dotenv import load_dotenv

load_dotenv()

solicitudes_instagram = 0 

def obtener_ultimos_posts(usuario, cantidad=5):
    global solicitudes_instagram
    L = instaloader.Instaloader()
    isnta_user=os.getenv('INSTA_USER')
    isnta_pass=os.getenv('INSTA_PASS')
    L.login(isnta_user, isnta_pass)
    solicitudes_instagram += 1
    posts = instaloader.Profile.from_username(L.context, usuario).get_posts()
    solicitudes_instagram += 1
    ultimos = []
    for idx, post in enumerate(posts):
        if idx >= cantidad:
            break
        ultimos.append({
            "url": post.url,
            "caption": post.caption,
            "fecha": post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
        })
    return ultimos, solicitudes_instagram

# Ejemplo de uso
if __name__ == "__main__":
    usuario = "instagram"  
    posts = obtener_ultimos_posts(usuario, cantidad=3)
    for post in posts:
        print(f"URL: {post['url']}\nDescripción: {post['caption']}\nFecha: {post['fecha']}\n")