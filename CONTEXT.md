# Contexto del Proyecto: Bot de Discord "La Villa"

## Descripción General
Bot de Discord privado para el servidor "La Villa". Diseñado para automatizar moderación, gestión de roles, canales de voz dinámicos, estadísticas y alertas de gaming.
Desplegado en VPS (Docker).

## Estructura del Proyecto
- **Lenguaje:** Python 3.11 (`discord.py`)
- **Gestión:** Docker Compose (`restart: always`)
- **Ruta VPS:** `/root/discord-bot`

## Funcionalidades Activas

### 1. Sistema de Bienvenida
- **Trigger:** Nuevo usuario entra al servidor.
- **Acción:**
    - Genera imagen personalizada con avatar.
    - Envía mensaje a `#bienvenida` mencionando al usuario y enlazando a `#roles`.

### 2. Auto-Roles (Botones)
- **Ubicación:** Canal `#roles`.
- **Roles:** `Gamers`, `Estudio`, `Invitados`.
- **Persistencia:** Los botones funcionan tras reinicios del bot.

### 3. Voz Dinámica
- **Trigger:** Usuario entra al canal de voz `➕ Crear Sala`.
- **Acción:** Crea un canal temporal privado.
- **Comando `!room`:** El creador puede renombrar su sala. El bot añade el prefijo `🔊 ` para identificarla.

### 4. Utilidades Sociales
- **`!poll`:** Genera encuestas con reacciones automáticas (1-10 opciones).
- **`!avatar`:** Muestra el avatar de alta resolución.
- **`!help`:** Embed dinámico con ayuda visual.
- **`!clear`:** Herramienta de moderación para limpiar mensajes.

### 5. Automatización Avanzada (Admin)
- **Roles Temporales (`!tempRole`):**
    - Asigna roles por un número de días determinado.
    - Persistencia en `temp_roles.json` (sobrevive reinicios).
    - Verificación automática cada 1 hora.
- **Gestión de Emojis (`!addEmoji`):**
    - Permite añadir emojis desde URLs externas o adjuntos directamente.

### 6. Estadísticas en Tiempo Real
- **Ubicación:** Canales de voz (bloqueados) en categoría INFORMACIÓN.
- **Métricas:** `👥 Miembros`, `🟢 Online`, `🎧 Activos`.
- **Actualización:** Cada 6 minutos (Loop task).

### 7. Gaming Hub (`#chat-gaming`)
- **Comando `!gaming`:**
    - **Uso:** `!gaming` (o `!Gaming`).
    - **Efecto:** Menciona al rol `@Gamers` con un mensaje de "Gaming Time".
    - **Restricción:** Solo funciona en canales llamados `chat-gaming`. Si se usa fuera, borra el mensaje del usuario y envía un error temporal (5 min).
- **Alertas de Stream:**
    - **Trigger:** Un usuario con rol `Gamers` comienza a transmitir (Twitch/YouTube).
    - **Acción:** Envía un aviso automático a `#chat-gaming` con el link del stream.

### 8. Soporte Multi-Servidor ("Open Source Santiago")
- **Capacidad:** El proyecto incluye scripts de mantenimiento para un segundo servidor.
- **Funciones:**
    - Reorganización de canales (Script `scripts/`).
    - Reparación de Onboarding (Docs).
    - Gestión de Roles masiva.

## Comandos de Mantenimiento (Admin)
- `!setup_roles`: Despliega el panel de botones (Solo Admin).
- `!setup_voice`: Configura el canal generador de salas (Solo Admin).

## Despliegue y Mantenimiento
- **Repositorio:** `https://github.com/pcastelo/discord-bot`
- **Host:** VPS (`212.85.15.125`)
- **Actualización:**
    ```bash
    ssh -i ~/.ssh/pihole root@212.85.15.125
    cd discord-bot
    git pull
    docker compose up -d --build
    ```
- **Ver Logs:** `docker logs -f lavilla-bot`

## Notas Técnicas
- **Intents:** Requiere `Presence`, `Server Members`, `Message Content` activados en Discord Developer Portal.
- **Case Insensitive:** El bot está configurado para ignorar mayúsculas/minúsculas en comandos.
