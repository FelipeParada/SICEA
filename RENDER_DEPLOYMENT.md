# Despliegue de SICEA en Render.com

Este documento contiene las instrucciones para desplegar el proyecto SICEA en Render.com.

## Archivos de Configuración Creados

1. **`backend/build.sh`** - Script de construcción para el backend Django
2. **`render.yaml`** - Configuración de infraestructura como código (Blueprint)

## Cambios Realizados

### Backend (Django)

1. **`requirements.txt`** - Agregados:
   - `gunicorn==23.0.0` - Servidor WSGI para producción
   - `whitenoise==6.8.2` - Para servir archivos estáticos

2. **`settings.py`** - Actualizaciones:
   - Variables de entorno para `SECRET_KEY`, `DEBUG`, y `ALLOWED_HOSTS`
   - Configuración de CORS dinámica
   - Configuración de archivos estáticos con WhiteNoise
   - Middleware de WhiteNoise agregado

## Pasos para Desplegar en Render.com

### 1. Preparar el Repositorio

Asegúrate de que todos los archivos estén en tu repositorio Git:

```bash
cd /home/chen/Documentos/Universidad/Semestre\ Delta/Ingeniería\ de\ Software\ II/Mi\ SICEA/SICEA
git add .
git commit -m "Configuración para despliegue en Render.com"
git push origin main
```

### 2. Crear Cuenta en Render.com

1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub/GitLab

### 3. Opción A: Despliegue con Blueprint (Recomendado)

1. En el dashboard de Render, haz clic en **"New +"** → **"Blueprint"**
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente el archivo `render.yaml`
4. Revisa la configuración de los servicios:
   - **sicea-db**: Base de datos PostgreSQL
   - **sicea-backend**: API Django
   - **sicea-frontend**: Aplicación React
5. Haz clic en **"Apply"**
6. Render creará automáticamente todos los servicios

### 4. Opción B: Despliegue Manual

#### Crear Base de Datos PostgreSQL

1. Click en **"New +"** → **"PostgreSQL"**
2. Nombre: `sicea-db`
3. Database: `siceadb`
4. User: `admin`
5. Region: `Oregon` (o la más cercana)
6. Plan: `Free`
7. Click **"Create Database"**

#### Crear Backend (Web Service)

1. Click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio
3. Configuración:
   - **Name**: `sicea-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn SICEAproject.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

4. Variables de entorno (Environment):
   ```
   SECRET_KEY=<genera-una-clave-secreta-aleatoria>
   DEBUG=False
   ALLOWED_HOSTS=*
   DB_HOST=<host-de-tu-base-de-datos>
   DB_NAME=siceadb
   DB_USER=admin
   DB_PASSWORD=<password-de-tu-base-de-datos>
   DB_PORT=5432
   CORS_ALLOWED_ORIGINS=https://<tu-frontend-url>.onrender.com
   ```

5. Dale permisos de ejecución al script build.sh:
   - En "Advanced" settings, agrega un comando pre-build:
   ```bash
   chmod +x build.sh
   ```

#### Crear Frontend (Static Site)

1. Click en **"New +"** → **"Static Site"**
2. Conecta tu repositorio
3. Configuración:
   - **Name**: `sicea-frontend`
   - **Root Directory**: `.`
   - **Build Command**: `cd frontend/sicea && npm install && npm run build`
   - **Publish Directory**: `frontend/sicea/dist`
   - **Plan**: `Free`

### 5. Configurar Variables de Entorno del Frontend

Después de desplegar el backend, necesitarás actualizar el frontend para que apunte a la URL correcta del backend.

1. En `frontend/sicea/src/services/config.ts`, actualiza la URL base:
   ```typescript
   export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://sicea-backend.onrender.com';
   ```

2. Agrega variable de entorno en Render para el frontend:
   ```
   VITE_API_URL=https://sicea-backend.onrender.com
   ```

### 6. Configuración Post-Despliegue

1. **Actualizar CORS en el Backend**:
   - Agrega la URL del frontend a `CORS_ALLOWED_ORIGINS`:
   ```
   CORS_ALLOWED_ORIGINS=https://<tu-frontend>.onrender.com,http://localhost:3000
   ```

2. **Crear Super Usuario**:
   - En el dashboard del backend, ve a "Shell"
   - Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

3. **Verificar Migraciones**:
   - Las migraciones se ejecutan automáticamente en el `build.sh`
   - Revisa los logs para confirmar que se ejecutaron correctamente

## Notas Importantes

### Limitaciones del Plan Free

- **Backend**: Se suspende después de 15 minutos de inactividad
- **Base de Datos**: 
  - 1 GB de almacenamiento
  - Se elimina después de 90 días de inactividad
  - No tiene backups automáticos

### Recomendaciones

1. **Backups**: Configura backups regulares de la base de datos
2. **Logs**: Monitorea los logs regularmente para detectar errores
3. **SSL**: Render proporciona SSL automáticamente
4. **Custom Domain**: Puedes configurar un dominio personalizado en la configuración del servicio

## Solución de Problemas

### El backend no inicia

- Verifica los logs en el dashboard de Render
- Asegúrate de que todas las variables de entorno estén configuradas
- Verifica que `build.sh` tenga permisos de ejecución

### Error de CORS

- Verifica que la URL del frontend esté en `CORS_ALLOWED_ORIGINS`
- Asegúrate de incluir `https://` en la URL

### Base de datos no conecta

- Verifica que las credenciales de la base de datos sean correctas
- Asegúrate de que `DB_HOST` apunte al host interno de Render
- En Render, usa la "Internal Database URL" para mejor rendimiento

### Frontend no carga

- Verifica que `VITE_API_URL` esté configurada correctamente
- Revisa la consola del navegador para errores
- Asegúrate de que el build command sea correcto

## URLs de Ejemplo

Después del despliegue, tus servicios estarán disponibles en:

- **Frontend**: `https://sicea-frontend.onrender.com`
- **Backend API**: `https://sicea-backend.onrender.com`
- **Admin Django**: `https://sicea-backend.onrender.com/admin`

## Mantenimiento

### Actualizar el Código

1. Haz push a tu repositorio:
   ```bash
   git push origin main
   ```
2. Render detectará automáticamente los cambios y redesplegará

### Re-desplegar Manualmente

En el dashboard de cada servicio, haz clic en **"Manual Deploy"** → **"Deploy latest commit"**

### Ver Logs

En el dashboard de cada servicio, ve a la pestaña **"Logs"** para ver los registros en tiempo real.

## Contacto y Soporte

- Documentación de Render: https://render.com/docs
- Comunidad: https://community.render.com/
