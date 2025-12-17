# 🏰 Bot de La Villa

Este es el bot privado del servidor **La Villa**. Aquí tienes la lista de comandos y funciones disponibles.

## 🎮 Comandos para Usuarios

### `!room [nombre]`
Personaliza el nombre de tu sala de voz temporal.
- **Uso:** `!room Cine de Terror`
- **Requisito:** Debes estar en tu sala creada con "➕ Crear Sala".

### `!poll "Pregunta" "Opcion 1" "Opcion 2"`
Crea una encuesta automática con reacciones.
- **Uso:** `!poll "¿Jugamos LoL?" "Si" "No" "Quizás"`
- **Nota:** Las opciones deben ir entre comillas.

### `!avatar @usuario`
Muestra la foto de perfil en grande de un usuario.

### `!help`
Muestra una lista bonita con todos los comandos disponibles.

---

## 🤖 Funciones Automáticas

| Función | Descripción |
| :--- | :--- |
| **👋 Bienvenida** | Te saluda con una imagen personalizada al entrar. |
| **🎙️ Crear Sala** | Únete a **"➕ Crear Sala"** para crear tu canal temporal. Puedes renombrarlo con `!room`. |
| **📺 Alerta Stream** | Si tienes el rol `Gamers` y prendes stream, el bot avisa en `#chat-gaming`. |
| **📊 Estadísticas** | Contadores en tiempo real: `Miembros`, `Online` y `🎧 Voz` (cada 6 min). |

---

## 🛡️ Comandos de Administración (Solo Admins)

Estos comandos son para configuración inicial y mantenimiento.

- **`!setup_roles`**: Crea el panel de botones para auto-asignarse roles.
- **`!setup_voice`**: Crea el canal generador de salas.
- **`!clear [n]`**: Borra los últimos `n` mensajes del chat (Ej: `!clear 10`).
- **`!tempRole "Rol" @Users 7`**: Asigna un rol (ej: "Vip") a usuarios por X días.
- **`!addEmoji nombre [URL/Adjunto]`**: Roba un emoji desde un enlace o subiendo la foto.

---

## 🛠️ Desarrollo

Desplegado en VPS mediante Docker.
Código fuente: [GitHub Repo](https://github.com/pcastelo/discord-bot)
