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
| **📊 Estadísticas** | Contadores en tiempo real: `Miembros`, `Online` y `🎧 Activos` (cada 6 min). |
| **🎭 Roles e Identidad** | Panel interactivo en `#roles`. (`Gamers`, `Estudio`). |
| **🔔 Notificaciones** | Panel "Opt-in" para alertas selectivas (Newsletter, Downtime). |

---

## 🛡️ Comandos de Administración (Solo Admins)

*Estos comandos se auto-destruyen tras ejecutarse para mantener el chat limpio.*

- **`!setup_roles`**: Despliega el panel de identidad (Gamers/Estudio).
- **`!setup_notifications`**: Despliega el panel de alertas del sistema.
- **`!setup_voice`**: Configura el canal generador de salas.
- **`!clear [n]`**: Borra los últimos `n` mensajes.
- **`!tempRole "Rol" @User 7`**: Asigna rol temporal (días).
- **`!addEmoji nombre [URL/Adjunto]`**: Clona emojis externos.
- **`!addSound nombre [Adjunto]`**: Sube sonidos al Soundboard.

### 🔒 Zona Admin (`#sudo`)
El servidor cuenta con una categoría oculta `ADMIN` para operaciones discretas y logs. Usa el canal `#sudo` para ejecutar comandos sensibles.

---

## 🛠️ Desarrollo

Desplegado en VPS mediante Docker.
Código fuente: [GitHub Repo](https://github.com/pcastelo/discord-bot)
