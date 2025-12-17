# 🏰 Bot de La Villa

Este es el bot privado del servidor **La Villa**. Aquí tienes la lista de comandos y funciones disponibles.

## 🎮 Comandos para Usuarios

### `!gaming`
Avisa a todos los **Gamers** para jugar.
- **Uso:** Escribe `!gaming` o `!Gaming`.
- **Dónde:** Solo funciona en el canal **`#chat-gaming`**.
- **Notas:** Si lo usas en otro canal, tu mensaje será borrado.

---

## 🤖 Funciones Automáticas

| Función | Descripción |
| :--- | :--- |
| **👋 Bienvenida** | Te saluda con una imagen personalizada al entrar. |
| **🎙️ Crear Sala** | Únete al canal de voz **"➕ Crear Sala"** para crear tu propio canal de voz temporal. |
| **📺 Alerta Stream** | Si tienes el rol `Gamers` y prendes stream (Twitch/YouTube), el bot avisa en `#chat-gaming`. |
| **📊 Estadísticas** | Mira cuánta gente hay conectada en los canales de arriba (`Miembros` / `Online`). |

---

## 🛡️ Comandos de Administración (Solo Admins)

Estos comandos son para configuración inicial y mantenimiento.

- **`!setup_roles`**: Crea el panel de botones para auto-asignarse roles en el canal actual.
- **`!setup_voice`**: Crea el canal de voz generador "Crear Sala" en la categoría GAMING.

---

## 🛠️ Desarrollo

Desplegado en VPS mediante Docker.
Código fuente: [GitHub Repo](https://github.com/pcastelo/discord-bot)
