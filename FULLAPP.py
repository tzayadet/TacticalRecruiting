#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APLICACIÓN INTEGRAL DE SELECCIÓN Y RECLUTAMIENTO
20 módulos completos + scoring R/S/T automático + perfiles IT especializados
⚠️  EJECUTA ESTE ÚNICO ARCHIVO. Sin dependencias externas.
"""

import sqlite3
import os
import sys
import shutil
import base64
from pathlib import Path
from datetime import datetime, timedelta
import re


# ========================================
# CONFIGURACIÓN GLOBAL
# ========================================

APP_DIR = Path.cwd() / "rrhh_app_data"
DB_PATH = APP_DIR / "database.db"
CVS_DIR = APP_DIR / "cvs"
APP_DIR.mkdir(exist_ok=True)
CVS_DIR.mkdir(exist_ok=True)

# Perfiles IT especializados (stack Alvatross/TM Forum)
PERFILES_IT = {
    'backend': 'Backend / Full Stack Developer',
    'frontend': 'Front-End Developer',
    'devops': 'DevOps / Cloud / Security Engineer',
    'qa': 'QA / Automation Engineer',
    'cloud': 'Cloud Engineer',
    'integrations': 'Integrations / API Specialist',
    'solution_architect': 'Solution / Software Architect',
    'product_owner': 'Product Owner / Product Manager',
    'support': 'Operations / Support Engineer'
}

SENIORITY_NIVELES = {
    'junior': 'Junior (1-3 años)',
    'mid': 'Mid (3-5 años)',
    'senior': 'Senior (5+ años)',
    'lead': 'Lead / Manager'
}

# Ponderación R/S/T por perfil (según guía Alvatross)
PONDERACION_RST = {
    'backend': (0.20, 0.60, 0.20),
    'devops': (0.20, 0.60, 0.20),
    'qa': (0.25, 0.50, 0.25),
    'solution_architect': (0.25, 0.50, 0.25),
    'product_owner': (0.30, 0.40, 0.30),
    'integrations': (0.20, 0.60, 0.20),
    'support': (0.30, 0.40, 0.30),
    'frontend': (0.25, 0.50, 0.25),
    'cloud': (0.20, 0.60, 0.20)
}


# ========================================
# UTILIDADES DE INTERFAZ
# ========================================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    input("\n↲ Pulsa Enter para continuar...")


def validar_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def formatear_fecha(fecha_str):
    """Convertir YYYY-MM-DD a DD/MM/YYYY"""
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return fecha.strftime("%d/%m/%Y")
    except:
        return fecha_str


# ========================================
# INICIALIZACIÓN DE BASE DE DATOS + DATOS REALES
# ========================================

def inicializar_db():
    """Crear esquema completo + sembrar datos reales de perfiles IT Alvatross"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla candidatos (con CV)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidatos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            linkedin TEXT,
            github TEXT,
            localizacion TEXT,
            remoto TEXT,
            disponibilidad TEXT,
            nivel_estudios TEXT,
            titulacion TEXT,
            certificaciones TEXT,
            idiomas TEXT,
            experiencia_total INTEGER DEFAULT 0,
            experiencia_telecom INTEGER DEFAULT 0,
            experiencia_tmforum TEXT,
            stack_lenguajes TEXT,
            stack_frameworks TEXT,
            stack_bbdd TEXT,
            stack_cloud TEXT,
            stack_devops TEXT,
            stack_apis TEXT,
            stack_mensajeria TEXT,
            competencias TEXT,
            salario_esperado TEXT,
            estado TEXT DEFAULT 'activo',
            perfil_it TEXT,
            seniority TEXT,
            cv_filename TEXT,
            gdpr_consent BOOLEAN DEFAULT 0,
            fecha_registro TEXT,
            origen TEXT DEFAULT 'manual',
            notas TEXT
        )
    ''')
    
    # Tabla vacantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacantes (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            departamento TEXT,
            ubicacion TEXT,
            modalidad TEXT,
            stack_obligatorio TEXT NOT NULL,
            stack_deseable TEXT,
            experiencia_tmforum TEXT,
            experiencia_telecom TEXT,
            rango_salarial_min INTEGER,
            rango_salarial_max INTEGER,
            responsable TEXT,
            urgencia TEXT DEFAULT 'media',
            candidatos_finalistas TEXT,
            candidato_seleccionado TEXT,
            estado TEXT DEFAULT 'abierta',
            fecha_apertura TEXT NOT NULL,
            notas TEXT
        )
    ''')
    
    # Tabla evaluaciones R/S/T (scoring automático)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id TEXT NOT NULL,
            vacante_id TEXT,
            fecha TEXT NOT NULL,
            evaluador TEXT NOT NULL,
            r_puntuacion INTEGER DEFAULT 0,
            r_notas TEXT,
            s_puntuacion INTEGER DEFAULT 0,
            s_notas TEXT,
            t_puntuacion INTEGER DEFAULT 0,
            t_notas TEXT,
            score_final REAL DEFAULT 0.0,
            senales_encaje TEXT,
            recomendacion TEXT,
            tipo_entrevista TEXT
        )
    ''')
    
    # Tabla preguntas entrevista (estructurado por perfil)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            subcategoria TEXT,
            texto TEXT NOT NULL,
            ejemplo_respuesta TEXT,
            nivel_dificultad TEXT DEFAULT 'medio',
            tags TEXT
        )
    ''')
    
    # Tabla perfiles empresa (con stack TM Forum/ODA real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles_empresa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            stack TEXT,
            responsabilidades TEXT,
            seniority TEXT,
            salario_min INTEGER,
            salario_max INTEGER,
            requisitos_obligatorios TEXT,
            requisitos_deseables TEXT,
            competencias_blandas TEXT,
            cultura_trabajo TEXT
        )
    ''')
    
    # Tabla asociaciones colaboración
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asociaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            contacto TEXT,
            web TEXT,
            notas TEXT
        )
    ''')
    
    # Tabla centros formación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS centros_formacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            contacto TEXT,
            web TEXT,
            direccion TEXT,
            convenio_activo BOOLEAN DEFAULT 0
        )
    ''')
    
    # Tabla estudiantes prácticas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes_practicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT,
            centro TEXT,
            carrera TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            tutor_empresa TEXT,
            estado TEXT DEFAULT 'pendiente',
            notas TEXT
        )
    ''')
    
    # Tabla portales empleo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portales_empleo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            url TEXT,
            tipo TEXT,
            coste TEXT,
            notas TEXT
        )
    ''')
    
    # Tabla plantillas vacantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plantillas_vacantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            departamento TEXT,
            ultima_actualizacion TEXT
        )
    ''')
    
    # Tabla team building
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_building (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            nombre_actividad TEXT NOT NULL,
            empresa_proveedora TEXT,
            precio_estimado TEXT,
            duracion TEXT,
            participantes_min INTEGER,
            participantes_max INTEGER,
            notas TEXT
        )
    ''')
    
    # Tabla normativa interna
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normativa_interna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha_aprobacion TEXT,
            version TEXT
        )
    ''')
    
    # Tabla tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            tipo TEXT DEFAULT 'tarea',
            prioridad TEXT DEFAULT 'media',
            fecha_limite TEXT,
            responsable TEXT,
            estado TEXT DEFAULT 'pendiente',
            completado BOOLEAN DEFAULT 0,
            fecha_creacion TEXT NOT NULL,
            recordatorio BOOLEAN DEFAULT 0
        )
    ''')
    
    # Tabla calendario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            duracion INTEGER DEFAULT 60,
            ubicacion TEXT,
            participantes TEXT,
            notas TEXT,
            email_enviado BOOLEAN DEFAULT 0,
            candidato_id TEXT,
            vacante_id TEXT
        )
    ''')
    
    # Tabla onboarding
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS onboarding (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            rrhh_notificado BOOLEAN DEFAULT 0,
            sistemas_notificado BOOLEAN DEFAULT 0,
            departamento_notificado BOOLEAN DEFAULT 0,
            equipo_asignado TEXT,
            notas TEXT,
            checklist TEXT DEFAULT '{}'
        )
    ''')
    
    # Tabla anotaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anotaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            contenido TEXT NOT NULL,
            categoria TEXT,
            fecha_creacion TEXT NOT NULL,
            ultima_modificacion TEXT
        )
    ''')
    
    # Tabla glosario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glosario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            termino TEXT NOT NULL UNIQUE,
            definicion TEXT NOT NULL,
            categoria TEXT
        )
    ''')
    
    # ========================================
    # SEMBRAR DATOS REALES DE ALVATROSS (perfiles IT especializados)
    # ========================================
    
    # Perfiles empresa con stack TM Forum/ODA real
    cursor.execute('SELECT COUNT(*) FROM perfiles_empresa')
    if cursor.fetchone()[0] == 0:
        perfiles = [
            ('Backend Developer', 
             'Desarrollo de microservicios y APIs REST para plataforma OSS',
             'Java 17, Spring Boot 3, PostgreSQL, Kubernetes, TM Forum Open APIs',
             'Desarrollo módulos OSS, APIs TM Forum, integración sistemas, resiliencia (timeouts/retries/circuit breakers)',
             'mid',
             35000,
             50000,
             'Java/Spring Boot (3+ años), APIs REST, microservicios, SQL, Docker/Kubernetes',
             'TM Forum Open APIs, ODA, Kafka, experiencia telecom OSS/BSS',
             'Comunicación técnica clara, ownership, trabajo en equipo, adaptabilidad',
             'Entorno DevSecOps, proyectos largo plazo, calidad código, documentación clara'),
            
            ('DevOps / Cloud / Security Engineer',
             'Automatización de despliegues y operaciones para plataforma OSS cloud-native',
             'Docker, Kubernetes, AWS/Azure, Terraform, GitLab CI, Prometheus/Grafana',
             'Pipelines CI/CD con controles seguridad, infraestructura cloud IaC, monitorización, DevSecOps',
             'mid',
             40000,
             55000,
             'Docker/Kubernetes (2+ años), CI/CD, cloud (AWS/Azure), IaC (Terraform/Ansible)',
             'Helm, ArgoCD, seguridad cloud, experiencia entornos regulados',
             'Automatiza por defecto, enfoque seguridad sin bloquear entregas, colaboración equipos',
             'Cultura DevSecOps, automatización máxima, documentación procesos, calidad operativa'),
            
            ('QA / Automation Engineer',
             'Aseguramiento de calidad mediante pruebas automatizadas para APIs TM Forum',
             'Selenium, Cypress, JUnit, Postman, Jenkins, REST APIs testing',
             'Diseño planes prueba APIs TM Forum, automatización integración, colaboración devs como habilitador',
             'mid',
             32000,
             45000,
             'Automatización pruebas (2+ años), APIs REST, testing microservicios, CI/CD',
             'TM Forum Open APIs, Postman Collections, contrato-first testing',
             'Pensamiento crítico, precisión, colabora como habilitador (no policía), comunicación clara',
             'Calidad sin bloquear velocidad, testing como habilitador, colaboración estrecha devs'),
            
            ('Integrations / API Specialist',
             'Conexión plataforma OSS con sistemas externos mediante estándares TM Forum',
             'REST, TM Forum Open APIs (SID, Party, Product Ordering), Kafka, RabbitMQ',
             'Desarrollo adaptadores, validación contratos APIs, troubleshooting integraciones, logs precisos',
             'mid',
             36000,
             52000,
             'Integraciones sistemas (2+ años), REST APIs, mensajería (Kafka/RabbitMQ)',
             'TM Forum Open APIs certificado, ODA, experiencia telecom OSS/BSS',
             'Precisión en contratos APIs y logs, piensa interoperabilidad desde diseño, comunicación técnica',
             'Enfoque en interoperabilidad, trazabilidad total, calidad contratos APIs, documentación clara'),
            
            ('Solution / Software Architect',
             'Diseño arquitecturas solución para proyectos OSS/BSS con clientes operadores',
             'Arquitectura ODA, microservicios, TM Forum APIs, patrones diseño, cloud-native',
             'Diseño sistemas escalables alto volumen, cumplimiento estándares TM Forum/ODA, gobernanza APIs',
             'senior',
             55000,
             75000,
             'Arquitectura microservicios (5+ años), APIs REST, patrones diseño, cloud',
             'TM Forum Open APIs certificado, ODA, experiencia telecom OSS/BSS complejos',
             'Visión sistémica, criterio técnico sólido, comunicación impecable no técnicos, mentoría',
             'Diseños coherentes estándares, escalabilidad, adaptabilidad, documentación excelente'),
            
            ('Product Owner / Product Manager',
             'Definición roadmap plataforma OSS alineado a necesidades operadores telecom',
             'Backlog management, Jira/Confluence, TM Forum estándares, OSS/BSS dominio',
             'Priorización funcionalidades, traducción negocio↔técnico, gestión stakeholders, métricas producto',
             'mid',
             42000,
             60000,
             'Gestión producto IT/telecom (3+ años), metodologías ágiles, herramientas (Jira)',
             'Conocimiento TM Forum/ODA, experiencia OSS/BSS, dominio telecom',
             'Claridad estructura foco valor, respeta límites técnicos, comunicación constante',
             'Colaboración estrecha equipos técnicos, enfoque valor negocio, priorización datos'),
            
            ('Operations / Support Engineer',
             'Soporte post-despliegue y resolución incidencias plataforma OSS para clientes',
             'Linux, bases de datos, redes, monitorización (Prometheus/Grafana), troubleshooting',
             'Monitorización 24/7, resolución incidencias críticas, comunicación clientes, documentación RCA',
             'mid',
             30000,
             42000,
             'Soporte sistemas (2+ años), Linux, BBDD, redes básicas, troubleshooting',
             'Experiencia OSS/BSS, conocimiento plataforma Alvatross, telecom',
             'Calma bajo presión, método sistemático (hipótesis→pruebas→acción), documenta para evitar recurrencias',
             'Enfoque en continuidad servicio, respuesta rápida incidencias, mejora continua procesos')
        ]
        cursor.executemany('''
            INSERT INTO perfiles_empresa (
                nombre, descripcion, stack, responsabilidades, seniority,
                salario_min, salario_max, requisitos_obligatorios, requisitos_deseables,
                competencias_blandas, cultura_trabajo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', perfiles)
    
    # Banco de preguntas estructurado por perfil (de documentos reales)
    cursor.execute('SELECT COUNT(*) FROM preguntas')
    if cursor.fetchone()[0] == 0:
        preguntas = [
            # General
            ('general', None, 'Cuéntame tu trayectoria profesional en los últimos 5 años', 'Busca narrativa coherente, progresión, motivaciones', 'medio', 'trayectoria,experiencia'),
            ('general', None, '¿Por qué estás interesado en esta oportunidad?', 'Busca motivación real, no respuesta genérica', 'medio', 'motivación,empresa'),
            ('general', None, '¿Qué sabes de nuestras soluciones OSS/BSS y APIs estándar?', 'Valida investigación previa sobre el core business', 'dificil', 'oss,bss,apis,investigación'),
            
            # Cultural
            ('cultural', None, 'Describe tu experiencia trabajando en equipos multidisciplinares (devs, QA, arquitectos, producto)', 'Busca colaboración real, no solo coexistencia', 'medio', 'colaboración,equipos'),
            ('cultural', None, 'En nuestra cultura valoramos proyectos de larga duración con clientes estables. ¿Cómo ves tu evolución profesional a 3-5 años?', 'Busca estabilidad vs. job hopping constante', 'medio', 'estabilidad,carrera'),
            ('cultural', None, '¿Cómo explicas decisiones técnicas complejas a perfiles no técnicos (producto, cliente)?', 'Busca claridad, empatía, adaptación al interlocutor', 'medio', 'comunicación,empatía'),
            
            # Situacional
            ('situacional', None, 'Estás en mitad de un sprint y descubres un bug crítico en producción. ¿Qué haces?', 'Busca protocolo: alerta equipo, rollback si necesario, análisis causa raíz, comunicación', 'dificil', 'crisis,producción,protocolo'),
            ('situacional', None, 'Un compañero critica constantemente tus PRs de forma poco constructiva. ¿Cómo actúas?', 'Busca asertividad, canalización por tech lead si persiste, enfoque en mejora', 'medio', 'conflicto,pr'),
            
            # Backend
            ('tecnica', 'backend', 'En un microservicio Java/Spring Boot, ¿cómo gestionarías la resiliencia ante fallos de dependencias externas?', 'Esperamos: circuit breakers (Resilience4j), timeouts, retries con backoff exponencial, fallbacks', 'dificil', 'resiliencia,microservicios,spring'),
            ('tecnica', 'backend', '¿Cómo diseñarías el versionado de APIs REST en un entorno OSS/BSS con múltiples clientes?', 'Esperamos: versionado en URL/header, estrategia de deprecated, contrato claro, documentación', 'medio', 'apis,versionado,contrato'),
            ('tecnica', 'backend', '¿Qué patrones aplicarías para evitar N+1 queries en una API que devuelve órdenes con sus líneas?', 'Esperamos: JOIN FETCH, EntityGraph, DTO projection, paginación', 'medio', 'optimización,queries,jpa'),
            ('tecnica', 'backend', '¿Cómo garantizarías la idempotencia en una API de provisión de servicios (ej: activar línea móvil)?', 'Esperamos: idempotency keys, registro de operaciones, validación previa a ejecución', 'dificil', 'idempotencia,transacciones'),
            
            # DevOps
            ('tecnica', 'devops', '¿Cómo diseñarías un pipeline GitLab CI para un microservicio con requerimientos de seguridad en entornos regulados?', 'Esperamos: SAST/DAST en pipeline, escaneo imágenes, firmado artefactos, aprobaciones manuales en prod, secrets management', 'dificil', 'cicd,seguridad,compliance'),
            ('tecnica', 'devops', 'Un despliegue en Kubernetes falla en el 30% de los pods. ¿Cuál es tu proceso de diagnóstico?', 'Esperamos: logs pods fallidos, events namespace, describe pod, readiness/liveness probes, recursos asignados', 'medio', 'kubernetes,debugging'),
            ('tecnica', 'devops', '¿Cómo gestionarías el secreto de una API de TM Forum en múltiples entornos sin exponerlo en código?', 'Esperamos: Vault/HashiCorp, Kubernetes Secrets con RBAC, variables entorno cifradas, nunca en repositorio', 'dificil', 'secrets,seguridad'),
            
            # QA
            ('tecnica', 'qa', '¿Cómo estructurarías la estrategia de testing para una API TM Forum Open API (ej: Product Ordering)?', 'Esperamos: contrato primero (OpenAPI spec), tests de contrato, happy path + edge cases, idempotencia, concurrencia', 'dificil', 'testing,apis,tmforum'),
            ('tecnica', 'qa', 'Un bug crítico pasa QA y llega a producción. ¿Qué harías tras detectarlo?', 'Esperamos: rollback inmediato si posible, análisis causa raíz (¿por qué falló QA?), mejora del proceso, no culpas', 'medio', 'calidad,mejora_continua'),
            
            # Integrations
            ('tecnica', 'integrations', '¿Qué información es crítica en los logs de una integración con un sistema legacy de provisión?', 'Esperamos: correlation ID, payload entrada/salida (sanitizado), timestamps, estado transaccional, errores técnicos vs negocio', 'medio', 'logs,integración,debugging'),
            ('tecnica', 'integrations', '¿Cómo manejarías la incompatibilidad de formatos entre una API REST moderna y un sistema SOAP legacy?', 'Esperamos: adapter pattern, transformación en middleware, validación contratos, logging exhaustivo', 'dificil', 'integración,legacy,transformación'),
            
            # Solution Architect
            ('tecnica', 'solution_architect', 'Un cliente exige alta disponibilidad (99.99%) para su plataforma OSS. ¿Qué elementos arquitectónicos propondrías?', 'Esperamos: multi-AZ/region, circuit breakers, rate limiting, cache layers, DB replication, chaos engineering, SLA monitoring', 'dificil', 'arquitectura,ha,escalabilidad'),
            ('tecnica', 'solution_architect', '¿Cómo justificarías técnicamente el uso de ODA frente a una arquitectura monolítica legacy?', 'Esperamos: agilidad time-to-market, reducción vendor lock-in, interoperabilidad TM Forum, capacidad evolutiva, TCO a largo plazo', 'dificil', 'oda,arquitectura,tmforum'),
            
            # Product Owner
            ('tecnica', 'product_owner', '¿Cómo priorizarías el backlog cuando el equipo tiene capacidad para 10 story points pero hay 30 puntos de demanda de negocio?', 'Esperamos: valor vs esfuerzo, RICE framework, alineación con OKRs trimestrales, transparencia con stakeholders', 'medio', 'priorización,backlog'),
            ('tecnica', 'product_owner', 'Un desarrollador dice que una user story es técnicamente inviable. ¿Cuál es tu siguiente paso?', 'Esperamos: entender limitación técnica real, buscar alternativas con dev/arquitecto, replantear valor vs solución, no imponer', 'medio', 'colaboración,técnico'),
            
            # Support
            ('tecnica', 'support', 'Recibes una alerta: "Tasa de error 5xx en API ProductOrdering > 5%". ¿Cuál es tu protocolo de actuación?', 'Esperamos: verificar alerta (no falso positivo), revisar métricas correlacionadas, identificar patrón (hora, cliente, endpoint), escalar a equipo técnico si persiste', 'dificil', 'incidentes,alertas,protocolo'),
            ('tecnica', 'support', 'Un cliente reporta que una orden de servicio está "atascada" en estado PENDING desde hace 2 horas. ¿Cómo investigas?', 'Esperamos: buscar order ID en logs, verificar estado en BD, revisar colas de mensajería (Kafka), contactar con equipo de integraciones si necesario', 'medio', 'soporte,debugging,clientes'),
        ]
        cursor.executemany('''
            INSERT INTO preguntas (categoria, subcategoria, texto, ejemplo_respuesta, nivel_dificultad, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', preguntas)
    
    # Asociaciones colaboración (reales)
    cursor.execute('SELECT COUNT(*) FROM asociaciones')
    if cursor.fetchone()[0] == 0:
        asociaciones = [
            ('Inserta', 'discapacidad', 'info@inserta.es', 'https://www.inserta.es', 'Fundación ONCE para inserción laboral personas con discapacidad'),
            ('Fundación Adecco', 'discapacidad', 'info@fundacionadecco.es', 'https://www.fundacionadecco.es', 'Inserción laboral colectivos vulnerables'),
            ('Mujeres Tech', 'mujeres', 'contacto@mujerestech.es', 'https://mujerestech.es', 'Comunidad mujeres en tecnología'),
            ('AdaLab', 'mujeres', 'hola@adalab.es', 'https://adalab.es', 'Formación tecnológica para mujeres'),
            ('FELGTB', 'lgtb', 'info@felgtb.org', 'https://www.felgtb.org', 'Federación Estatal LGTBI+'),
            ('CERMI', 'discapacidad', 'cermi@cermi.es', 'https://www.cermi.es', 'Comité Representante Personas con Discapacidad')
        ]
        cursor.executemany('''
            INSERT INTO asociaciones (nombre, tipo, contacto, web, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', asociaciones)
    
    # Centros formación (reales)
    cursor.execute('SELECT COUNT(*) FROM centros_formacion')
    if cursor.fetchone()[0] == 0:
        centros = [
            ('Universidad Politécnica de Madrid', 'universidad', 'practicas@upm.es', 'https://www.upm.es', 'Madrid'),
            ('Universidad Carlos III de Madrid', 'universidad', 'empresas.leganes@uc3m.es', 'https://www.uc3m.es', 'Madrid'),
            ('Universidad de Oviedo', 'universidad', 'practicas@uniovi.es', 'https://www.uniovi.es', 'Gijón'),
            ('IES Virgen de la Paloma', 'fp', 'secretaria@iesvirgendelapaloma.es', 'https://iesvirgendelapaloma.educa.madrid.org', 'Madrid'),
            ('IES La Magdalena', 'fp', 'ieslamagdalena@eduastur.es', 'https://ieslamagdalena.edu', 'Avilés'),
            ('IE Business School', 'negocio', 'careers@ie.edu', 'https://www.ie.edu', 'Madrid'),
            ('Portal Universia', 'colocacion', 'info@universia.es', 'https://www.universia.es', 'España')
        ]
        cursor.executemany('''
            INSERT INTO centros_formacion (nombre, tipo, contacto, web, direccion)
            VALUES (?, ?, ?, ?, ?)
        ''', centros)
    
    # Portales empleo (reales)
    cursor.execute('SELECT COUNT(*) FROM portales_empleo')
    if cursor.fetchone()[0] == 0:
        portales = [
            ('LinkedIn Jobs', 'https://linkedin.com/jobs', 'general', 'Premium Recruiter', 'Alta visibilidad IT'),
            ('InfoJobs', 'https://www.infojobs.net', 'general', 'Bolsa completa', 'Alto volumen candidatos España'),
            ('Tecnoempleo', 'https://www.tecnoempleo.com', 'IT', 'Gratuito/Pro', 'Especializado IT/Telecom'),
            ('Stack Overflow Jobs', 'https://stackoverflow.com/jobs', 'IT', 'Gratuito', 'Talento técnico senior'),
            ('GitHub Jobs', 'https://jobs.github.com', 'IT', 'Gratuito', 'Desarrolladores open source'),
            ('Indeed', 'https://www.indeed.es', 'general', 'Gratuito/Publicidad', 'Alto volumen general')
        ]
        cursor.executemany('''
            INSERT INTO portales_empleo (nombre, url, tipo, coste, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', portales)
    
    # Team building (reales)
    cursor.execute('SELECT COUNT(*) FROM team_building')
    if cursor.fetchone()[0] == 0:
        actividades = [
            ('deporte', 'Escape Room Tecnológico', 'EscapeKings', '25€/persona', '2 horas', 4, 8, 'Resolución problemas en equipo con temática ciberseguridad'),
            ('gastronomia', 'Taller cocina colaborativa', 'Cook&Team', '45€/persona', '3 horas', 6, 20, 'Elaboración menú completo en equipos rotativos'),
            ('naturaleza', 'Ruta senderismo + picnic', 'AireLibre', '15€/persona', '5 horas', 10, 30, 'Ruta guiada por Sierra de Guadarrama'),
            ('cultura', 'Visita Museo Reina Sofía + taller', 'ArteEnEquipo', '20€/persona', '4 horas', 8, 25, 'Recorrido obras + taller creatividad'),
            ('solidaridad', 'Voluntariado huerto urbano', 'HuertosSolidarios', 'Donación', '3 horas', 5, 15, 'Mantenimiento huerto para comedores sociales')
        ]
        cursor.executemany('''
            INSERT INTO team_building (categoria, nombre_actividad, empresa_proveedora, precio_estimado, duracion, participantes_min, participantes_max, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', actividades)
    
    # Normativa interna (reales)
    cursor.execute('SELECT COUNT(*) FROM normativa_interna')
    if cursor.fetchone()[0] == 0:
        normativas = [
            ('Código Ético Anticorrupción', 'anticorrupcion', 'Política de tolerancia cero ante sobornos, regalos inapropiados y conflictos de interés. Obligatorio reporting anónimo de irregularidades.', '2023-01-15', 'v2.1'),
            ('Protocolo Inclusión Discapacidad', 'discapacidad', 'Adaptaciones razonables en procesos de selección y puesto de trabajo. Colaboración con Inserta y Fundación Adecco para inserción laboral.', '2023-03-20', 'v1.5'),
            ('Política Diversidad LGTB+', 'lgtb', 'Compromiso con entornos seguros e inclusivos. Prohibición discriminación por orientación sexual e identidad de género. Alianza con FELGTB.', '2023-06-10', 'v1.2')
        ]
        cursor.executemany('''
            INSERT INTO normativa_interna (titulo, tipo, contenido, fecha_aprobacion, version)
            VALUES (?, ?, ?, ?, ?)
        ''', normativas)
    
    # Glosario (términos reales OSS/BSS)
    cursor.execute('SELECT COUNT(*) FROM glosario')
    if cursor.fetchone()[0] == 0:
        terminos = [
            ('API', 'Application Programming Interface: interfaz que permite la comunicación entre sistemas', 'técnico'),
            ('DevOps', 'Cultura y conjunto de prácticas que unen desarrollo y operaciones para acelerar entregas', 'metodologia'),
            ('GDPR', 'Reglamento General de Protección de Datos de la UE. Marco legal para tratamiento datos personales', 'legal'),
            ('Kanban', 'Método ágil de gestión visual del trabajo con límites WIP (Work In Progress)', 'metodologia'),
            ('Microservicios', 'Arquitectura de software donde una aplicación se estructura como conjunto de servicios pequeños e independientes', 'técnico'),
            ('ODA', 'Open Digital Architecture: marco de referencia de TM Forum para arquitecturas digitales abiertas', 'telecom'),
            ('OSS', 'Operational Support Systems: sistemas que gestionan operaciones de red y servicios en telecomunicaciones', 'telecom'),
            ('Scrum', 'Framework ágil con sprints, roles definidos (PO, SM, Dev Team) y ceremonias estructuradas', 'metodologia'),
            ('SLA', 'Service Level Agreement: acuerdo de nivel de servicio que define expectativas entre proveedor y cliente', 'legal'),
            ('Time to Hire', 'Métrica RRHH: tiempo transcurrido desde apertura vacante hasta aceptación oferta', 'rrhh'),
            ('TM Forum', 'Asociación global que define estándares para operadores de telecomunicaciones (Open APIs, ODA)', 'telecom'),
            ('BSS', 'Business Support Systems: sistemas que gestionan procesos comerciales y relacionados con el cliente', 'telecom')
        ]
        cursor.executemany('''
            INSERT INTO glosario (termino, definicion, categoria)
            VALUES (?, ?, ?)
        ''', terminos)
    
    conn.commit()
    conn.close()


# ========================================
# CRUD CANDIDATOS (con gestión real de CVs + scoring R/S/T)
# ========================================

def crear_candidato():
    limpiar_pantalla()
    print("=" * 70)
    print("   🆕 REGISTRAR NUEVO CANDIDATO (+ CV)")
    print("=" * 70)
    print("\n💡 Stack especializado: APIs estándar, OSS/BSS, Java/Spring, Kubernetes")
    
    datos = {}
    while not datos.get('nombre'):
        datos['nombre'] = input("\nNombre completo*: ").strip()
        if not datos['nombre']:
            print("⚠️  El nombre es obligatorio")
    
    while True:
        datos['email'] = input("Email: ").strip()
        if not datos['email'] or validar_email(datos['email']):
            break
        print("⚠️  Email no válido. Ejemplo: nombre@dominio.com")
    
    datos['telefono'] = input("Teléfono: ").strip()
    datos['linkedin'] = input("LinkedIn URL: ").strip()
    datos['github'] = input("GitHub URL: ").strip()
    datos['localizacion'] = input("Ciudad/Provincia: ").strip()
    datos['remoto'] = input("Disponibilidad remoto (Total/Parcial/Presencial): ").strip()
    datos['disponibilidad'] = input("Disponibilidad incorporación: ").strip()
    datos['nivel_estudios'] = input("Nivel de estudios: ").strip()
    datos['titulacion'] = input("Titulación específica: ").strip()
    datos['certificaciones'] = input("Certificaciones relevantes: ").strip()
    datos['idiomas'] = input("Idiomas: ").strip()
    
    try:
        datos['experiencia_total'] = int(input("Años totales en IT: ").strip() or "0")
    except ValueError:
        datos['experiencia_total'] = 0
    
    try:
        datos['experiencia_telecom'] = int(input("Años en telecom/OSS/BSS: ").strip() or "0")
    except ValueError:
        datos['experiencia_telecom'] = 0
    
    datos['experiencia_tmforum'] = input("Experiencia con APIs estándar/TM Forum/ODA (Sí/No/Nivel): ").strip()
    datos['stack_lenguajes'] = input("Lenguajes (ej: Java, Python, TypeScript): ").strip()
    datos['stack_frameworks'] = input("Frameworks (ej: Spring Boot, Angular, React): ").strip()
    datos['stack_bbdd'] = input("Bases de datos: ").strip()
    datos['stack_cloud'] = input("Cloud (AWS/Azure/GCP): ").strip()
    datos['stack_devops'] = input("DevOps (Docker, Kubernetes...): ").strip()
    datos['stack_apis'] = input("APIs/Integración (REST, TM Forum, SOAP...): ").strip()
    datos['stack_mensajeria'] = input("Mensajería (Kafka, RabbitMQ...): ").strip()
    datos['competencias'] = input("Competencias blandas: ").strip()
    datos['salario_esperado'] = input("Expectativa salarial (k€): ").strip()
    
    print("\nPerfiles IT:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    datos['perfil_it'] = input("\nPerfil IT*: ").strip().lower()
    while datos['perfil_it'] not in PERFILES_IT:
        print("⚠️  Perfil no válido. Elige uno de la lista anterior.")
        datos['perfil_it'] = input("Perfil IT*: ").strip().lower()
    
    print("\nSeniority:")
    for key, value in SENIORITY_NIVELES.items():
        print(f"  {key:10} - {value}")
    datos['seniority'] = input("\nSeniority*: ").strip().lower()
    while datos['seniority'] not in SENIORITY_NIVELES:
        print("⚠️  Seniority no válido. Elige uno de la lista.")
        datos['seniority'] = input("Seniority*: ").strip().lower()
    
    # Subir CV
    datos['cv_filename'] = None
    print("\n¿Deseas adjuntar CV? (S/n): ", end="")
    if input().strip().lower() in ('', 's', 'si', 'y', 'yes'):
        ruta_cv = input("Ruta completa al archivo CV (PDF/DOC/DOCX): ").strip()
        if ruta_cv and os.path.exists(ruta_cv):
            ext = os.path.splitext(ruta_cv)[1].lower()
            if ext in ['.pdf', '.doc', '.docx']:
                candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
                nuevo_nombre = f"{candidato_id}_{os.path.basename(ruta_cv)}"
                destino = CVS_DIR / nuevo_nombre
                
                try:
                    shutil.copy2(ruta_cv, destino)
                    datos['cv_filename'] = nuevo_nombre
                    print(f"✅ CV guardado correctamente en: {destino.name}")
                except Exception as e:
                    print(f"⚠️  Error guardando CV: {e}")
            else:
                print("⚠️  Formato no soportado. Solo PDF, DOC o DOCX.")
        else:
            print("⚠️  Archivo no encontrado.")
    
    datos['notas'] = input("\nNotas iniciales (stack específico, proyectos OSS/BSS...): ").strip()
    gdpr = input("\n✅ Consentimiento GDPR registrado? (S/n): ").strip().lower()
    datos['gdpr_consent'] = 1 if gdpr in ('', 's', 'si', 'yes') else 0
    datos['origen'] = 'manual'
    datos['estado'] = 'activo'
    datos['fecha_registro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar en BD
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    cursor.execute('''
        INSERT INTO candidatos (
            id, nombre, email, telefono, linkedin, github, localizacion,
            remoto, disponibilidad, nivel_estudios, titulacion, certificaciones,
            idiomas, experiencia_total, experiencia_telecom, experiencia_tmforum,
            stack_lenguajes, stack_frameworks, stack_bbdd, stack_cloud,
            stack_devops, stack_apis, stack_mensajeria, competencias, salario_esperado,
            estado, perfil_it, seniority, cv_filename, gdpr_consent,
            fecha_registro, origen, notas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        candidato_id,
        datos['nombre'],
        datos['email'],
        datos['telefono'],
        datos['linkedin'],
        datos['github'],
        datos['localizacion'],
        datos['remoto'],
        datos['disponibilidad'],
        datos['nivel_estudios'],
        datos['titulacion'],
        datos['certificaciones'],
        datos['idiomas'],
        datos['experiencia_total'],
        datos['experiencia_telecom'],
        datos['experiencia_tmforum'],
        datos['stack_lenguajes'],
        datos['stack_frameworks'],
        datos['stack_bbdd'],
        datos['stack_cloud'],
        datos['stack_devops'],
        datos['stack_apis'],
        datos['stack_mensajeria'],
        datos['competencias'],
        datos['salario_esperado'],
        datos['estado'],
        datos['perfil_it'],
        datos['seniority'],
        datos['cv_filename'],
        datos['gdpr_consent'],
        datos['fecha_registro'],
        datos['origen'],
        datos['notas']
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Candidato registrado correctamente")
    print(f"   ID: {candidato_id}")
    print(f"   Nombre: {datos['nombre']}")
    print(f"   Perfil: {PERFILES_IT[datos['perfil_it']]} ({datos['seniority'].upper()})")
    if datos['cv_filename']:
        print(f"   📎 CV: {datos['cv_filename']}")
    pausa()


def listar_candidatos():
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 LISTAR CANDIDATOS")
    print("=" * 70)
    
    buscar = input("\nBuscar (nombre, stack) - Deja en blanco para todos: ").strip()
    estado = input("Filtrar por estado (activo/inactivo/archivado) - Deja en blanco: ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT id, nombre, email, telefono, stack_lenguajes, perfil_it, seniority, estado, cv_filename, score_final FROM candidatos WHERE estado != 'eliminado'"
    params = []
    
    condiciones = []
    if estado and estado != 'todos':
        condiciones.append(f"estado = '{estado}'")
    
    if buscar:
        condiciones.append(f"(nombre LIKE '%{buscar}%' OR stack_lenguajes LIKE '%{buscar}%')")
    
    if condiciones:
        query += " AND " + " AND ".join(condiciones)
    
    query += " ORDER BY fecha_registro DESC"
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No se encontraron candidatos.")
        pausa()
        return
    
    print(f"\n📊 Encontrados: {len(resultados)} candidatos\n")
    print(f"{'ID':<15} {'Nombre':<25} {'Perfil':<25} {'Seniority':<10} {'Score':<8} {'CV':<5}")
    print("-" * 95)
    
    for row in resultados:
        cv_icon = "📎" if row[8] else "  "
        perfil = PERFILES_IT.get(row[5], row[5])[:25] if row[5] else '-'
        score = f"{row[9]:.1f}" if row[9] else "-"
        print(f"{row[0]:<15} {row[1][:23]:<25} {perfil:<25} {row[6] or '-':<10} {score:<8} {cv_icon:<5}")
    
    pausa()


def ver_detalle_candidato():
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  DETALLE DE CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM candidatos WHERE id = ?', (cid,))
    candidato = cursor.fetchone()
    
    if not candidato:
        conn.close()
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\n📄 FICHA COMPLETA: {candidato['nombre']}")
    print(f"{'='*70}")
    print(f"ID:          {candidato['id']}")
    print(f"Email:       {candidato['email'] or '-'}")
    print(f"Teléfono:    {candidato['telefono'] or '-'}")
    print(f"LinkedIn:    {candidato['linkedin'] or '-'}")
    print(f"GitHub:      {candidato['github'] or '-'}")
    print(f"📍 Ubicación: {candidato['localizacion'] or '-'} | Remoto: {candidato['remoto'] or '-'}")
    print(f"📅 Incorporación: {candidato['disponibilidad'] or '-'}")
    
    print(f"\n🎓 Formación:")
    print(f"   Estudios:    {candidato['nivel_estudios'] or '-'}")
    print(f"   Titulación:  {candidato['titulacion'] or '-'}")
    print(f"   Certificaciones: {candidato['certificaciones'] or '-'}")
    print(f"   Idiomas:     {candidato['idiomas'] or '-'}")
    
    print(f"\n💼 Experiencia:")
    print(f"   Total IT:    {candidato['experiencia_total']} años")
    print(f"   Telecom OSS/BSS: {candidato['experiencia_telecom']} años")
    print(f"   TM Forum/ODA: {candidato['experiencia_tmforum'] or 'Sin experiencia'}")
    
    print(f"\n🛠️  Stack técnico:")
    print(f"   Lenguajes:   {candidato['stack_lenguajes'] or '-'}")
    print(f"   Frameworks:  {candidato['stack_frameworks'] or '-'}")
    print(f"   BBDD:        {candidato['stack_bbdd'] or '-'}")
    print(f"   Cloud:       {candidato['stack_cloud'] or '-'}")
    print(f"   DevOps:      {candidato['stack_devops'] or '-'}")
    print(f"   APIs:        {candidato['stack_apis'] or '-'}")
    print(f"   Mensajería:  {candidato['stack_mensajeria'] or '-'}")
    
    print(f"\n🌟 Competencias: {candidato['competencias'] or '-'}")
    print(f"💰 Salario esperado: {candidato['salario_esperado'] or '-'}")
    print(f"👤 Perfil IT: {PERFILES_IT.get(candidato['perfil_it'], candidato['perfil_it'] or '-')}")
    print(f"⭐ Seniority: {SENIORITY_NIVELES.get(candidato['seniority'], candidato['seniority'] or '-')}")
    
    cv_path = CVS_DIR / candidato['cv_filename'] if candidato['cv_filename'] else None
    print(f"\n📎 CV: {'✅ Disponible' if cv_path and cv_path.exists() else '⚠️  No disponible'}")
    if cv_path and cv_path.exists():
        print(f"   Ruta: {cv_path}")
    
    print(f"\n📝 Notas:")
    print(f"   {candidato['notas'] or '-'}")
    
    print(f"\n🛡️  GDPR: {'✅ Consentimiento registrado' if candidato['gdpr_consent'] else '⚠️  Pendiente'}")
    print(f"📅 Registro: {candidato['fecha_registro']}")
    print(f"🏷️  Estado: {candidato['estado']}")
    
    # Mostrar evaluaciones R/S/T
    print(f"\n{'='*70}")
    print("📊 EVALUACIONES R/S/T - Sistema de Scoring Automático")
    print(f"{'='*70}")
    
    cursor.execute('''
        SELECT * FROM evaluaciones 
        WHERE candidato_id = ? 
        ORDER BY fecha DESC
    ''', (cid,))
    evaluaciones = cursor.fetchall()
    
    if not evaluaciones:
        print("📭 Sin evaluaciones registradas aún.")
    else:
        for e in evaluaciones:
            print(f"\n[{e['fecha']}] Evaluador: {e['evaluador']}")
            print(f"   R (Comunicación): {e['r_puntuacion']}/10 | {e['r_notas'] or '-'}")
            print(f"   S (Técnica):      {e['s_puntuacion']}/10 | {e['s_notas'] or '-'}")
            print(f"   T (Cultural):     {e['t_puntuacion']}/10 | {e['t_notas'] or '-'}")
            print(f"   ➤ Score final:    {e['score_final']:.2f}/10 | Recomendación: {e['recomendacion']}")
            if e['senales_encaje']:
                print(f"   ✅ Señales: {e['senales_encaje']}")
    
    conn.close()
    pausa()


def descargar_cv():
    limpiar_pantalla()
    print("=" * 70)
    print("   📥 DESCARGAR/VER CV DE CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, cv_filename FROM candidatos WHERE id = ?', (cid,))
    resultado = cursor.fetchone()
    conn.close()
    
    if not resultado or not resultado[1]:
        print("\n❌ Candidato no encontrado o CV no adjuntado.")
        pausa()
        return
    
    nombre, cv_filename = resultado
    cv_path = CVS_DIR / cv_filename
    
    if not cv_path.exists():
        print(f"\n❌ Archivo CV no encontrado: {cv_filename}")
        print("   Posible causa: archivo eliminado manualmente de la carpeta 'cvs'")
        pausa()
        return
    
    print(f"\n📄 CV de: {nombre}")
    print(f"   Archivo: {cv_filename}")
    print(f"   Ruta completa: {cv_path.absolute()}")
    print("\n💡 Para abrirlo:")
    print("   • Windows: copia la ruta y pégala en el Explorador de archivos")
    print("   • Mac/Linux: abre terminal y ejecuta 'open' o 'xdg-open' con la ruta")
    pausa()


# ========================================
# CRUD VACANTES (con stack TM Forum/ODA)
# ========================================

def crear_vacante():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ CREAR NUEVA VACANTE")
    print("=" * 70)
    print("\n💡 Stack especializado: APIs estándar, OSS/BSS, cloud-native")
    
    datos = {}
    datos['titulo'] = input("\nTítulo del puesto*: ").strip()
    while not datos['titulo']:
        print("⚠️  El título es obligatorio")
        datos['titulo'] = input("Título del puesto*: ").strip()
    
    datos['departamento'] = input("Departamento (Desarrollo/DevOps/Producto/Arquitectura/Operaciones): ").strip()
    datos['ubicacion'] = input("Ubicación (Madrid/Avilés/Remoto): ").strip()
    datos['modalidad'] = input("Modalidad (Remoto_Total/Remoto_Parcial/Presencial): ").strip()
    
    print("\n--- Requisitos técnicos ---")
    datos['stack_obligatorio'] = input("Stack obligatorio* (ej: Java/Spring Boot, TM Forum APIs, Kubernetes): ").strip()
    while not datos['stack_obligatorio']:
        print("⚠️  El stack obligatorio es obligatorio")
        datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    
    datos['stack_deseable'] = input("Stack deseable (ej: AWS, Kafka, Terraform): ").strip()
    datos['experiencia_tmforum'] = input("Experiencia TM Forum/ODA (Obligatorio/Deseable/No_relevante): ").strip()
    datos['experiencia_telecom'] = input("Experiencia Telecom OSS/BSS (Obligatorio/Deseable/No_relevante): ").strip()
    
    print("\n--- Condiciones de contratación ---")
    try:
        datos['rango_salarial_min'] = int(input("Rango salarial mínimo (k€)*: ").strip())
    except ValueError:
        print("⚠️  Valor numérico requerido. Usando 0.")
        datos['rango_salarial_min'] = 0
    
    try:
        datos['rango_salarial_max'] = int(input("Rango salarial máximo (k€)*: ").strip())
    except ValueError:
        print("⚠️  Valor numérico requerido. Usando 0.")
        datos['rango_salarial_max'] = 0
    
    datos['responsable'] = input("Responsable de selección (RRHH)*: ").strip()
    while not datos['responsable']:
        print("⚠️  El responsable es obligatorio")
        datos['responsable'] = input("Responsable de selección (RRHH)*: ").strip()
    
    print("\nUrgencia:")
    print("  alta | media | baja")
    datos['urgencia'] = input("Urgencia: ").strip().lower() or 'media'
    if datos['urgencia'] not in ['alta', 'media', 'baja']:
        datos['urgencia'] = 'media'
    
    datos['notas'] = input("\nNotas adicionales (stack específico, cliente...): ").strip()
    datos['estado'] = 'abierta'
    datos['fecha_apertura'] = datetime.now().strftime("%Y-%m-%d")
    datos['candidatos_finalistas'] = ''
    datos['candidato_seleccionado'] = ''
    
    # Generar ID único
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM vacantes WHERE id LIKE ?', (f"VAC-{datetime.now().year}%",))
    count = cursor.fetchone()[0] + 1
    vacante_id = f"VAC-{datetime.now().year}-{count:03d}"
    
    cursor.execute('''
        INSERT INTO vacantes (
            id, titulo, departamento, ubicacion, modalidad,
            stack_obligatorio, stack_deseable, experiencia_tmforum, experiencia_telecom,
            rango_salarial_min, rango_salarial_max,
            responsable, urgencia, candidatos_finalistas,
            candidato_seleccionado, estado, fecha_apertura, notas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        vacante_id,
        datos['titulo'],
        datos['departamento'],
        datos['ubicacion'],
        datos['modalidad'],
        datos['stack_obligatorio'],
        datos['stack_deseable'],
        datos['experiencia_tmforum'],
        datos['experiencia_telecom'],
        datos['rango_salarial_min'],
        datos['rango_salarial_max'],
        datos['responsable'],
        datos['urgencia'],
        datos['candidatos_finalistas'],
        datos['candidato_seleccionado'],
        datos['estado'],
        datos['fecha_apertura'],
        datos['notas']
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Vacante creada correctamente")
    print(f"   ID: {vacante_id}")
    print(f"   Puesto: {datos['titulo']}")
    print(f"   Stack: {datos['stack_obligatorio']}")
    print(f"   Urgencia: {datos['urgencia'].upper()}")
    pausa()


def listar_vacantes():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 LISTAR VACANTES")
    print("=" * 70)
    
    estado = input("\nFiltrar por estado (abierta/cerrada) - Deja en blanco para todas: ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if estado:
        cursor.execute('SELECT id, titulo, departamento, ubicacion, urgencia, estado FROM vacantes WHERE estado = ? ORDER BY fecha_apertura DESC', (estado,))
    else:
        cursor.execute('SELECT id, titulo, departamento, ubicacion, urgencia, estado FROM vacantes ORDER BY fecha_apertura DESC')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay vacantes con esos criterios.")
        pausa()
        return
    
    print(f"\n📊 Encontradas: {len(resultados)} vacantes\n")
    print(f"{'ID':<15} {'Título':<30} {'Departamento':<20} {'Ubicación':<15} {'Urgencia':<10} {'Estado':<10}")
    print("-" * 100)
    
    for row in resultados:
        print(f"{row[0]:<15} {row[1][:28]:<30} {row[2] or '-':<20} {row[3] or '-':<15} {row[4]:<10} {row[5]:<10}")
    
    pausa()


# ========================================
# EVALUACIONES R/S/T - Scoring automático con ponderación por perfil
# ========================================

def crear_evaluacion():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ NUEVA EVALUACIÓN R/S/T - Scoring Automático")
    print("=" * 70)
    print("\n📌 R = Entrevista/Comunicación | S = Técnica/Stack | T = Cultural/Soft Skills")
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, perfil_it, stack_lenguajes FROM candidatos WHERE id = ?', (cid,))
    candidato = cursor.fetchone()
    
    if not candidato:
        conn.close()
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato[0]}")
    print(f"Perfil: {PERFILES_IT.get(candidato[1], candidato[1])}")
    print(f"Stack: {candidato[2] or '-'}")
    
    vid = input("\nID de la vacante (opcional): ").strip()
    if vid:
        cursor.execute('SELECT titulo FROM vacantes WHERE id = ?', (vid,))
        vacante = cursor.fetchone()
        if vacante:
            print(f"Vacante: {vacante[0]}")
        else:
            print("⚠️  Vacante no encontrada. Continuando sin asociar.")
            vid = None
    
    evaluador = input("\nEvaluador (tu nombre): ").strip()
    
    print("\n--- Dimensión R: Entrevista/Comunicación (1-10) ---")
    print("   1-3: respuestas vagas, sin ejemplos, confusión conceptos base")
    print("   4-6: base correcta, algunos ejemplos, huecos puntuales")
    print("   7-8: sólido, ejemplos claros, buena toma decisiones")
    print("   9-10: excelente, liderazgo/ownership, profundidad, anticipa riesgos")
    try:
        r_puntuacion = int(input("Puntuación R (1-10)*: ").strip())
    except ValueError:
        r_puntuacion = 0
    r_notas = input("Notas R: ").strip()
    
    print("\n--- Dimensión S: Técnica/Stack (1-10) ---")
    print("   Evalúa stack específico: APIs estándar, Java/Spring, Kubernetes...")
    try:
        s_puntuacion = int(input("Puntuación S (1-10)*: ").strip())
    except ValueError:
        s_puntuacion = 0
    s_notas = input("Notas S: ").strip()
    
    print("\n--- Dimensión T: Cultural/Soft Skills (1-10) ---")
    print("   Alineación DevSecOps, colaboración equipos multidisciplinares, estabilidad")
    try:
        t_puntuacion = int(input("Puntuación T (1-10)*: ").strip())
    except ValueError:
        t_puntuacion = 0
    t_notas = input("Notas T: ").strip()
    
    # Calcular score final con ponderación por perfil
    perfil = candidato[1] or 'backend'
    p_r, p_s, p_t = PONDERACION_RST.get(perfil, (0.25, 0.50, 0.25))
    score_final = round((r_puntuacion * p_r) + (s_puntuacion * p_s) + (t_puntuacion * p_t), 2)
    
    print(f"\n➤ Score final calculado: {score_final}/10 (ponderación {perfil}: R{p_r*100:.0f}% S{p_s*100:.0f}% T{p_t*100:.0f}%)")
    
    # Señales de buen encaje según perfil
    senales = []
    if perfil == 'backend':
        senales = ["Explica decisiones técnicas con datos", "Piensa en resiliencia (timeouts/retries/circuit breakers)", "Conoce prácticas calidad (tests/code review)"]
    elif perfil == 'devops':
        senales = ["Automatiza por defecto (IaC, pipelines)", "Enfoca seguridad sin bloquear entregas (DevSecOps)"]
    elif perfil == 'qa':
        senales = ["Pensamiento crítico y precisión", "Colabora como habilitador (no policía)"]
    elif perfil == 'integrations':
        senales = ["Precisión en contratos APIs y logs", "Piensa interoperabilidad desde diseño"]
    elif perfil == 'solution_architect':
        senales = ["Visión sistémica y criterio técnico sólido", "Documentación útil y comunicación impecable"]
    elif perfil == 'product_owner':
        senales = ["Claridad, estructura, foco en valor", "Respeta límites técnicos"]
    elif perfil == 'support':
        senales = ["Calma bajo presión y método sistemático", "Documenta para evitar recurrencias"]
    
    if senales:
        print("\n✅ Señales de buen encaje (marca las que observes):")
        senales_seleccionadas = []
        for i, senal in enumerate(senales, 1):
            if input(f"  [{i}] {senal} (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', ''):
                senales_seleccionadas.append(senal)
        senales_encaje = " | ".join(senales_seleccionadas) if senales_seleccionadas else ""
    else:
        senales_encaje = ""
    
    print("\n--- Recomendación final ---")
    print("  1. Contratar")
    print("  2. Reservas (seguir evaluando)")
    print("  3. Siguiente fase")
    print("  4. Descartar")
    rec_map = {"1": "contratar", "2": "reservas", "3": "siguiente_fase", "4": "descartar"}
    rec_opcion = input("Opción (1-4): ").strip()
    recomendacion = rec_map.get(rec_opcion, "reservas")
    
    cursor.execute('''
        INSERT INTO evaluaciones (
            candidato_id, vacante_id, fecha, evaluador,
            r_puntuacion, r_notas,
            s_puntuacion, s_notas,
            t_puntuacion, t_notas,
            score_final, senales_encaje, recomendacion, tipo_entrevista
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        cid,
        vid if vid else None,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        evaluador,
        r_puntuacion, r_notas,
        s_puntuacion, s_notas,
        t_puntuacion, t_notas,
        score_final,
        senales_encaje,
        recomendacion,
        'general'
    ))
    
    # Actualizar estado del candidato según score
    if score_final >= 8.5:
        cursor.execute('UPDATE candidatos SET estado = ? WHERE id = ?', ('finalista', cid))
    elif score_final >= 7.0:
        cursor.execute('UPDATE candidatos SET estado = ? WHERE id = ?', ('entrevista', cid))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Evaluación registrada correctamente")
    print(f"   Score final: {score_final}/10")
    print(f"   Recomendación: {recomendacion}")
    if senales_encaje:
        print(f"   ✅ Señales: {senales_encaje}")
    pausa()


# ========================================
# MÓDULOS 3-20 (implementaciones completas y especializadas)
# ========================================

def modulo_preguntas():
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   ❓ BANCO DE PREGUNTAS DE ENTREVISTA")
        print("=" * 70)
        print("\n1. 🔍 Buscar preguntas por perfil/perfil IT")
        print("2. 📋 Listar todas las preguntas")
        print("3. 🎯 Generar guía de entrevista (perfil IT)")
        print("4. ➕ Añadir nueva pregunta")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            buscar_preguntas()
        elif opcion == "2":
            listar_todas_preguntas()
        elif opcion == "3":
            generar_guia_entrevista()
        elif opcion == "4":
            anadir_pregunta()
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def buscar_preguntas():
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 BUSCAR PREGUNTAS POR PERFIL IT")
    print("=" * 70)
    
    print("\nPerfiles IT:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    
    perfil = input("\nPerfil IT (ej: backend, devops) o 'general' para todas: ").strip().lower()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if perfil == 'general' or not perfil:
        cursor.execute('SELECT * FROM preguntas ORDER BY categoria, nivel_dificultad DESC')
    else:
        cursor.execute('''
            SELECT * FROM preguntas 
            WHERE subcategoria = ? OR categoria = 'general' OR categoria = 'cultural' OR categoria = 'situacional'
            ORDER BY categoria, nivel_dificultad DESC
        ''', (perfil,))
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No se encontraron preguntas para este perfil.")
        pausa()
        return
    
    print(f"\n📊 Encontradas: {len(resultados)} preguntas\n")
    
    categoria_actual = None
    for p in resultados:
        if p[1] != categoria_actual:
            categoria_actual = p[1]
            print(f"\n{'='*70}")
            print(f"📌 CATEGORÍA: {categoria_actual.upper()}")
            if p[2]:
                print(f"   Subcategoría: {p[2]}")
            print('='*70)
        
        nivel = p[5][:1].upper() if p[5] else '?'
        print(f"\n[ID: {p[0]}] ({nivel})")
        print(f"❓ {p[3]}")
        if p[4]:
            print(f"💡 Ejemplo: {p[4][:70]}...")
        if p[6]:
            print(f"🏷️  Tags: {p[6]}")
    
    pausa()


def listar_todas_preguntas():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 TODAS LAS PREGUNTAS")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM preguntas ORDER BY categoria, subcategoria, nivel_dificultad DESC')
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay preguntas en el banco.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(resultados)} preguntas\n")
    
    categoria_actual = None
    for p in resultados:
        if p[1] != categoria_actual:
            categoria_actual = p[1]
            print(f"\n{'='*70}")
            print(f"📌 {categoria_actual.upper()}")
            print('='*70)
        
        sub = f" | {p[2]}" if p[2] else ""
        nivel = p[5][:1].upper() if p[5] else '?'
        print(f"\n[ID: {p[0]}] ({nivel}){sub}")
        print(f"❓ {p[3]}")
        if p[4]:
            print(f"💡 {p[4][:80]}...")
    
    pausa()


def generar_guia_entrevista():
    limpiar_pantalla()
    print("=" * 70)
    print("   🎯 GUÍA DE ENTREVISTA POR PERFIL - Stack Especializado")
    print("=" * 70)
    
    print("\nPerfiles IT:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    
    perfil = input("\nPerfil IT para la guía*: ").strip().lower()
    while perfil not in PERFILES_IT:
        print("⚠️  Perfil no válido")
        perfil = input("Perfil IT para la guía*: ").strip().lower()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener preguntas técnicas del perfil + generales/culturales
    cursor.execute('''
        SELECT * FROM preguntas 
        WHERE (subcategoria = ? AND categoria = 'tecnica') 
           OR categoria IN ('general', 'cultural', 'situacional')
        ORDER BY 
            CASE categoria 
                WHEN 'tecnica' THEN 1 
                WHEN 'general' THEN 2 
                WHEN 'cultural' THEN 3 
                WHEN 'situacional' THEN 4 
            END,
            nivel_dificultad DESC
        LIMIT 12
    ''', (perfil,))
    
    preguntas = cursor.fetchall()
    conn.close()
    
    if not preguntas:
        print("\n📭 No se pudieron generar preguntas para este perfil.")
        pausa()
        return
    
    print(f"\n{'='*70}")
    print(f"📄 GUÍA DE ENTREVISTA: {PERFILES_IT[perfil]}")
    print(f"{'='*70}")
    
    seccion_actual = None
    for i, p in enumerate(preguntas, 1):
        if p[1] != seccion_actual:
            seccion_actual = p[1]
            print(f"\n{'─'*70}")
            print(f"🔹 {seccion_actual.upper()}")
            print('─'*70)
        
        print(f"\n{i}. {p[3]}")
        if p[4]:
            print(f"   💡 {p[4][:80]}...")
    
    print(f"\n{'='*70}")
    print("💡 Tips:")
    print("   • Para perfiles técnicos: profundiza en resiliencia y APIs estándar")
    print("   • Para culturales: enfatiza estabilidad y trabajo en equipo largo plazo")
    print("   • Siempre pregunta sobre experiencia OSS/BSS y estándares APIs")
    print(f"{'='*70}")
    
    pausa()


def anadir_pregunta():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ AÑADIR NUEVA PREGUNTA")
    print("=" * 70)
    
    print("\nCategorías: general | tecnica | cultural | situacional")
    categoria = input("\nCategoría*: ").strip().lower()
    while categoria not in ['general', 'tecnica', 'cultural', 'situacional']:
        print("⚠️  Categoría no válida")
        categoria = input("Categoría*: ").strip().lower()
    
    subcategoria = None
    if categoria == 'tecnica':
        print("\nPerfiles: backend | devops | qa | integrations | frontend | cloud | solution_architect | product_owner | support")
        subcategoria = input("Subcategoría: ").strip().lower()
    
    texto = input("\nPregunta*: ").strip()
    while not texto:
        print("⚠️  La pregunta no puede estar vacía")
        texto = input("Pregunta*: ").strip()
    
    ejemplo = input("Ejemplo de respuesta esperada: ").strip()
    print("\nNivel dificultad: facil | medio | dificil")
    nivel = input("Nivel dificultad [medio]: ").strip().lower() or 'medio'
    
    tags = input("Tags (separados por comas): ").strip()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO preguntas (categoria, subcategoria, texto, ejemplo_respuesta, nivel_dificultad, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (categoria, subcategoria, texto, ejemplo, nivel, tags))
    conn.commit()
    conn.close()
    
    print("\n✅ Pregunta añadida correctamente.")
    pausa()


def modulo_perfiles_empresa():
    limpiar_pantalla()
    print("=" * 70)
    print("   👥 PERFILES SELECCIONADOS POR LA EMPRESA")
    print("=" * 70)
    print("\n💡 Perfiles especializados en stack OSS/BSS y APIs estándar TM Forum/ODA\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM perfiles_empresa ORDER BY seniority, nombre')
    perfiles = cursor.fetchall()
    conn.close()
    
    if not perfiles:
        print("\n📭 No hay perfiles definidos aún.")
        pausa()
        return
    
    for p in perfiles:
        print(f"\n{'─'*70}")
        print(f"🔹 {p[1].upper()} ({p[5].upper()})")
        print(f"   💰 Rango salarial: {p[6]}k - {p[7]}k €")
        print(f"\n   {p[2]}")
        print(f"\n   🛠️  Stack: {p[3]}")
        print(f"   📋 Responsabilidades: {p[4]}")
        print(f"\n   ⚙️  Obligatorio: {p[8]}")
        print(f"   ➕ Deseable: {p[9]}")
        print(f"\n   🌟 Soft Skills: {p[10]}")
        print(f"   🏢 Cultura: {p[11]}")
    
    print(f"\n{'─'*70}")
    pausa()


def modulo_presentacion_empresa():
    limpiar_pantalla()
    print("=" * 70)
    print("   🏢 PRESENTACIÓN DE EMPRESA")
    print("=" * 70)
    print("""
ALVATROSS (Grupo SATEC)

Somos una empresa tecnológica especializada en soluciones de software para 
la automatización de operaciones en telecomunicaciones, con enfoque en OSS 
(Operational Support Systems) y plataformas digitales modernas.

Pertenencia al Grupo SATEC:
• Grupo tecnológico español con más de 25 años de experiencia
• Presencia en proyectos globales (>15 países)
• Solidez organizativa y comercial consolidada

Plataforma OSS:
• Cloud-native y modular
• Basada en estándares TM Forum Open APIs y ODA
• Gestión integral: catálogo, inventario, orquestación, provisión
• Despliegue flexible: cloud o on-premise

Stack tecnológico:
• Arquitectura microservicios
• APIs REST conformes a TM Forum
• Compatibilidad multi-BBDD (Oracle, PostgreSQL, MySQL...)
• DevOps y automatización de despliegues

Oficinas:
• Madrid (Avenida de Europa, Aravaca)
• Avilés, Asturias

Cultura:
• Colaborativa y técnica
• Orientada a soluciones reales y aplicadas
• Proyectos de medio/largo plazo
• Reconocida como "Great Place to Work"
""")
    print("=" * 70)
    pausa()


def modulo_metodologias_agiles():
    limpiar_pantalla()
    print("=" * 70)
    print("   🚀 METODOLOGÍAS ÁGILES")
    print("=" * 70)
    print("""
SCRUM
• Iteraciones en sprints de 1-4 semanas
• Roles: Product Owner, Scrum Master, Development Team
• Eventos: Planning, Daily, Review, Retrospective
• Artefactos: Product Backlog, Sprint Backlog, Increment
• Clave: Transparencia, inspección y adaptación

KANBAN
• Flujo continuo visualizado en tablero
• Límites WIP (Work In Progress)
• Sin roles fijos ni sprints
• Métricas: Lead Time, Cycle Time
• Clave: Optimizar flujo y entrega continua

LEAN
• Filosofía centrada en valor y eliminación de desperdicios
• Principios: entregar rápido, empoderar equipo, ver el sistema completo
• Clave: Maximizar valor, minimizar waste

EXTREME PROGRAMMING (XP)
• Enfoque en calidad técnica
• Prácticas: TDD, Pair Programming, Integración Continua, Refactoring
• Clave: Código limpio y adaptación rápida

SAFe (Scaled Agile Framework)
• Escalado de ágil para grandes organizaciones
• Niveles: Equipo → Programa → Solución → Portafolio
• Clave: Coordinación entre múltiples equipos ágiles
""")
    print("=" * 70)
    pausa()


def modulo_convenio_madrid():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 CONVENIO COLECTIVO OFICINAS Y DESPACHOS DE MADRID")
    print("=" * 70)
    print("""
Vigencia: 2023-2026

Grupos profesionales y salarios base mensuales (2024):
• Grupo 1 (Directivos): 2.800€ - 3.500€
• Grupo 2 (Técnicos superiores): 2.200€ - 2.800€
• Grupo 3 (Técnicos medios): 1.800€ - 2.200€
• Grupo 4 (Administrativos cualificados): 1.500€ - 1.800€
• Grupo 5 (Administrativos): 1.300€ - 1.500€
• Grupo 6 (Auxiliares): 1.100€ - 1.300€

Jornada laboral:
• 1.792 horas anuales (40 horas semanales)
• Horario flexible con núcleo de presencia 10:00-15:00
• Viernes intensivo permitido por acuerdo empresa

Vacaciones:
• 22 días naturales + 6 días retribuidos recuperables
• Plus vacaciones: 300€ brutos anuales

Plus transporte: 35€/mes
Plus alimentación: 9€/día laborable (ticket restaurante)

Actualización salarial 2024: +3.5% IPC real

⚠️  Nota: Consultar texto completo oficial para casos específicos.
Documento oficial: https://www.mscbs.gob.es/
""")
    print("=" * 70)
    pausa()


def modulo_estatuto_trabajadores():
    limpiar_pantalla()
    print("=" * 70)
    print("   📜 ESTATUTO DE LOS TRABAJADORES (Real Decreto Legislativo 2/2015)")
    print("=" * 70)
    print("""
Artículos más relevantes para RRHH:

ARTÍCULO 40 - Movilidad funcional y geográfica
• Cambios de puesto dentro mismo grupo profesional: sin consentimiento
• Cambios a grupo inferior: requiere consentimiento o extinción con indemnización
• Traslados geográficos >25km: derecho a extinción con 20 días/año (máx. 12 meses)

ARTÍCULO 50 - Extinción por voluntad del trabajador
• Preaviso: según convenio (normalmente 15 días)
• Derecho a finiquito en 30 días

ARTÍCULO 53 - Despido disciplinario
• Causas: ineptitud, falta de adaptación, faltas de asistencia >20% en 2 meses
• Indemnización: 0 días (si procedente)
• Impugnación: 20 días hábiles desde notificación

ARTÍCULO 54 - Despido objetivo
• Causas: económicas, técnicas, organizativas, de producción
• Indemnización: 20 días/año (máx. 12 meses)
• Preaviso: 15 días

ARTÍCULO 55 - Faltas y sanciones
• Leves: apercibimiento, multa hasta 1 día
• Graves: suspensión 2-15 días
• Muy graves: suspensión 16-60 días o despido

ARTÍCULO 35 - Horas extraordinarias
• Máximo 80 horas/año (salvo fuerza mayor)
• Compensación: descanso o retribución económica

⚠️  Nota: Siempre consultar con asesoría jurídica para casos concretos.
Texto completo: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11453
""")
    print("=" * 70)
    pausa()


def modulo_asociaciones():
    limpiar_pantalla()
    print("=" * 70)
    print("   ♿ ASOCIACIONES CON LAS QUE COLABORAR")
    print("=" * 70)
    
    print("\nTipos disponibles: discapacidad | mujeres | lgtb | otras")
    tipo = input("\nFiltrar por tipo (deja en blanco para todas): ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute('SELECT * FROM asociaciones WHERE tipo = ? ORDER BY nombre', (tipo,))
    else:
        cursor.execute('SELECT * FROM asociaciones ORDER BY tipo, nombre')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay asociaciones con esos criterios.")
        pausa()
        return
    
    tipo_actual = None
    for a in resultados:
        if a[2] != tipo_actual:
            tipo_actual = a[2]
            print(f"\n{'='*70}")
            print(f"📌 TIPO: {tipo_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {a[1]}")
        print(f"   📧 Contacto: {a[3]}")
        print(f"   🌐 Web: {a[4]}")
        print(f"   ℹ️  {a[5]}")
    
    pausa()


def modulo_centros_formacion():
    limpiar_pantalla()
    print("=" * 70)
    print("   🎓 CENTROS DE ESTUDIOS, NEGOCIOS Y PRÁCTICAS")
    print("=" * 70)
    
    print("\nTipos: universidad | fp | negocio | colocacion")
    tipo = input("\nFiltrar por tipo (deja en blanco para todos): ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute('SELECT * FROM centros_formacion WHERE tipo = ? ORDER BY nombre', (tipo,))
    else:
        cursor.execute('SELECT * FROM centros_formacion ORDER BY tipo, nombre')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay centros con esos criterios.")
        pausa()
        return
    
    tipo_actual = None
    for c in resultados:
        if c[2] != tipo_actual:
            tipo_actual = c[2]
            print(f"\n{'='*70}")
            print(f"📌 TIPO: {tipo_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {c[1]}")
        print(f"   📍 {c[5]}")
        print(f"   📧 {c[3]}")
        print(f"   🌐 {c[4]}")
        print(f"   {'✅ Convenio activo' if c[6] else '⚠️  Sin convenio'}")
    
    pausa()


def modulo_estudiantes_practicas():
    limpiar_pantalla()
    print("=" * 70)
    print("   👨‍🎓 ESTUDIANTES DE PRÁCTICAS")
    print("=" * 70)
    
    estado = input("\nFiltrar por estado (pendiente/activo/finalizado) - Deja en blanco para todos: ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if estado:
        cursor.execute('SELECT * FROM estudiantes_practicas WHERE estado = ? ORDER BY fecha_inicio DESC', (estado,))
    else:
        cursor.execute('SELECT * FROM estudiantes_practicas ORDER BY fecha_inicio DESC')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay estudiantes registrados.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(resultados)} estudiantes\n")
    for e in resultados:
        print(f"\n🔹 {e[1]}")
        print(f"   📧 {e[2]}")
        print(f"   🎓 {e[4]} en {e[3]}")
        print(f"   📅 {formatear_fecha(e[5])} → {formatear_fecha(e[6]) if e[6] else '-'}")
        print(f"   👔 Tutor empresa: {e[7] or '-'}")
        print(f"   🏷️  Estado: {e[8]}")
        if e[9]:
            print(f"   ℹ️  {e[9]}")
    
    pausa()


def modulo_portales_empleo():
    limpiar_pantalla()
    print("=" * 70)
    print("   💼 PORTALES DE EMPLEO")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM portales_empleo ORDER BY tipo, nombre')
    portales = cursor.fetchall()
    conn.close()
    
    if not portales:
        print("\n📭 No hay portales registrados aún.")
        pausa()
        return
    
    tipo_actual = None
    for p in portales:
        if p[3] != tipo_actual:
            tipo_actual = p[3]
            print(f"\n{'='*70}")
            print(f"📌 TIPO: {tipo_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {p[1]}")
        print(f"   🌐 {p[2]}")
        print(f"   💰 Coste: {p[4]}")
        print(f"   ℹ️  {p[5]}")
    
    pausa()


def modulo_plantillas_vacantes():
    limpiar_pantalla()
    print("=" * 70)
    print("   📄 PLANTILLAS DE VACANTES PARA PUBLICAR")
    print("=" * 70)
    print("""
Plantillas predefinidas para publicación rápida:

BACKEND DEVELOPER (Java/Spring + TM Forum APIs)
───────────────────────────────────────────────────────────────────────
¿Quieres desarrollar software crítico para operadores de telecom?
Buscamos Backend Developer para unirse a nuestro equipo de producto OSS.

Stack: Java 17, Spring Boot 3, PostgreSQL, Kubernetes, TM Forum Open APIs
Metodología: Scrum + DevOps (GitLab CI/CD)
Modalidad: 100% remoto o híbrido (Madrid/Avilés)

Requisitos:
• 3+ años experiencia Java/Spring en entornos cloud
• Experiencia con microservicios y APIs REST/TM Forum
• Conocimientos de SQL y bases de datos relacionales
• Inglés técnico (B2 mínimo)

Ofrecemos:
• Salario: 38.000€ - 52.000€ (según experiencia)
• Proyectos estables de largo plazo con clientes internacionales
• Formación continua en estándares TM Forum y ODA
• Equipo técnico senior y ambiente colaborativo

───────────────────────────────────────────────────────────────────────

DEVOPS ENGINEER (Cloud + DevSecOps)
───────────────────────────────────────────────────────────────────────
¿Automatizas por naturaleza? Únete a nuestro equipo de plataforma OSS.

Stack: Docker, Kubernetes, AWS/Azure, Terraform, GitLab CI/CD, Prometheus
Modalidad: 100% remoto

Requisitos:
• 2+ años experiencia en DevOps/cloud
• Dominio de Kubernetes y pipelines CI/CD
• Automatización con Terraform/Ansible
• Mentalidad DevSecOps

Ofrecemos:
• Salario: 42.000€ - 58.000€
• Infraestructura cloud gestionada con IaC
• Proyectos OSS/BSS para operadores globales
• Formación certificaciones cloud (AWS/Azure)

───────────────────────────────────────────────────────────────────────

💡 Consejo: Personaliza estas plantillas con stack específico de cada vacante
antes de publicar en portales de empleo.
""")
    print("=" * 70)
    pausa()


def modulo_team_building():
    limpiar_pantalla()
    print("=" * 70)
    print("   🤝 TEAM BUILDING POR CATEGORÍAS")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT categoria FROM team_building ORDER BY categoria')
    categorias = [row[0] for row in cursor.fetchall()]
    
    print("\nCategorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        cursor.execute('SELECT COUNT(*) FROM team_building WHERE categoria = ?', (cat,))
        count = cursor.fetchone()[0]
        print(f"  {i}. {cat.capitalize()} ({count} actividades)")
    
    print("\n0. Ver todas las actividades")
    opcion = input("\n➤ Selecciona categoría (número) o 0 para todas: ").strip()
    
    if opcion == "0":
        cursor.execute('SELECT * FROM team_building ORDER BY categoria, nombre_actividad')
        actividades = cursor.fetchall()
    else:
        try:
            idx = int(opcion) - 1
            categoria_sel = categorias[idx]
            cursor.execute('SELECT * FROM team_building WHERE categoria = ? ORDER BY nombre_actividad', (categoria_sel,))
            actividades = cursor.fetchall()
        except (ValueError, IndexError):
            print("\n⚠️  Opción no válida.")
            conn.close()
            pausa()
            return
    
    conn.close()
    
    if not actividades:
        print("\n📭 No hay actividades en esta categoría.")
        pausa()
        return
    
    categoria_actual = None
    for a in actividades:
        if a[1] != categoria_actual:
            categoria_actual = a[1]
            print(f"\n{'='*70}")
            print(f"📌 CATEGORÍA: {categoria_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {a[2]}")
        print(f"   Empresa: {a[3]}")
        print(f"   💶 Precio: {a[4]} | ⏱️  Duración: {a[5]}")
        print(f"   👥 Participantes: {a[6]}-{a[7]} personas")
        print(f"   ℹ️  {a[8]}")
    
    pausa()


def modulo_normativa_interna():
    limpiar_pantalla()
    print("=" * 70)
    print("   📜 NORMATIVA INTERNA")
    print("=" * 70)
    
    print("\nTipos: anticonrrupcion | discapacidad | lgtb | otro")
    tipo = input("\nFiltrar por tipo (deja en blanco para todas): ").strip().lower() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute('SELECT * FROM normativa_interna WHERE tipo = ? ORDER BY fecha_aprobacion DESC', (tipo,))
    else:
        cursor.execute('SELECT * FROM normativa_interna ORDER BY fecha_aprobacion DESC')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay normativas registradas.")
        pausa()
        return
    
    tipo_actual = None
    for n in resultados:
        if n[2] != tipo_actual:
            tipo_actual = n[2]
            print(f"\n{'='*70}")
            print(f"📌 TIPO: {tipo_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {n[1]} (v{n[5]})")
        print(f"   📅 Aprobado: {n[4]}")
        print(f"   ℹ️  {n[3]}")
    
    pausa()


def modulo_tareas():
    limpiar_pantalla()
    print("=" * 70)
    print("   ✅ TAREAS PENDIENTES, OBJETIVOS Y ALARMAS")
    print("=" * 70)
    print("\n💡 Funcionalidad básica implementada:")
    print("   • Crear tareas con prioridad y fecha límite")
    print("   • Marcar tareas como completadas")
    print("   • Listar tareas pendientes ordenadas por fecha")
    print("\n1. ➕ Crear nueva tarea")
    print("2. 📋 Listar tareas pendientes")
    print("3. ✅ Marcar tarea como completada")
    print("0. ⬅️  Volver")
    
    opcion = input("\n➤ Opción: ").strip()
    
    if opcion == "1":
        crear_tarea()
    elif opcion == "2":
        listar_tareas_pendientes()
    elif opcion == "3":
        completar_tarea()


def crear_tarea():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ CREAR NUEVA TAREA")
    print("=" * 70)
    
    titulo = input("\nTítulo*: ").strip()
    while not titulo:
        print("⚠️  El título es obligatorio")
        titulo = input("Título*: ").strip()
    
    descripcion = input("Descripción: ").strip()
    
    print("\nTipo: tarea | objetivo | alarma")
    tipo = input("Tipo [tarea]: ").strip().lower() or 'tarea'
    if tipo not in ['tarea', 'objetivo', 'alarma']:
        tipo = 'tarea'
    
    print("\nPrioridad: baja | media | alta")
    prioridad = input("Prioridad [media]: ").strip().lower() or 'media'
    if prioridad not in ['baja', 'media', 'alta']:
        prioridad = 'media'
    
    fecha_limite = input("Fecha límite (YYYY-MM-DD, opcional): ").strip()
    if fecha_limite:
        try:
            datetime.strptime(fecha_limite, "%Y-%m-%d")
        except ValueError:
            print("⚠️  Formato de fecha no válido. Se omitirá.")
            fecha_limite = None
    
    responsable = input("Responsable: ").strip()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tareas (titulo, descripcion, tipo, prioridad, fecha_limite, responsable, estado, fecha_creacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, tipo, prioridad, fecha_limite, responsable, 'pendiente', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    
    print("\n✅ Tarea creada correctamente.")
    pausa()


def listar_tareas_pendientes():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 TAREAS PENDIENTES")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, titulo, tipo, prioridad, fecha_limite, responsable 
        FROM tareas 
        WHERE estado = 'pendiente' 
        ORDER BY 
            CASE prioridad 
                WHEN 'alta' THEN 1 
                WHEN 'media' THEN 2 
                WHEN 'baja' THEN 3 
            END,
            fecha_limite ASC NULLS LAST
    ''')
    tareas = cursor.fetchall()
    conn.close()
    
    if not tareas:
        print("\n📭 No hay tareas pendientes.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(tareas)} tareas pendientes\n")
    for t in tareas:
        fecha = t[4] if t[4] else "Sin fecha"
        resp = t[5] if t[5] else "Sin asignar"
        print(f"[{t[0]}] {t[1]}")
        print(f"   Tipo: {t[2]} | Prioridad: {t[3].upper()} | Fecha: {fecha} | Responsable: {resp}")
        print()
    
    pausa()


def completar_tarea():
    limpiar_pantalla()
    print("=" * 70)
    print("   ✅ MARCAR TAREA COMO COMPLETADA")
    print("=" * 70)
    
    tid = input("\nID de la tarea: ").strip()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE tareas SET estado = "completada", completado = 1 WHERE id = ? AND estado = "pendiente"', (tid,))
    if cursor.rowcount > 0:
        print("\n✅ Tarea marcada como completada.")
    else:
        print("\n⚠️  Tarea no encontrada o ya completada.")
    conn.commit()
    conn.close()
    pausa()


def modulo_calendario():
    limpiar_pantalla()
    print("=" * 70)
    print("   📅 CALENDARIO, CITAS Y AUTOMATIZACIÓN")
    print("=" * 70)
    print("\n💡 Funcionalidad básica implementada:")
    print("   • Programar entrevistas y reuniones")
    print("   • Listar citas próximas")
    print("   • Notas y participantes por cita")
    print("\n1. ➕ Programar nueva cita")
    print("2. 📋 Listar citas (hoy + próximos 7 días)")
    print("0. ⬅️  Volver")
    
    opcion = input("\n➤ Opción: ").strip()
    
    if opcion == "1":
        programar_cita()
    elif opcion == "2":
        listar_citas_proximas()


def programar_cita():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ PROGRAMAR NUEVA CITA")
    print("=" * 70)
    
    titulo = input("\nTítulo*: ").strip()
    while not titulo:
        print("⚠️  El título es obligatorio")
        titulo = input("Título*: ").strip()
    
    print("\nTipo: entrevista | reunion | otro")
    tipo = input("Tipo [entrevista]: ").strip().lower() or 'entrevista'
    if tipo not in ['entrevista', 'reunion', 'otro']:
        tipo = 'entrevista'
    
    fecha_hora = input("Fecha y hora (YYYY-MM-DD HH:MM)*: ").strip()
    while True:
        try:
            datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("⚠️  Formato no válido. Ejemplo: 2026-02-15 10:30")
            fecha_hora = input("Fecha y hora (YYYY-MM-DD HH:MM)*: ").strip()
    
    try:
        duracion = int(input("Duración en minutos [60]: ").strip() or "60")
    except ValueError:
        duracion = 60
    
    ubicacion = input("Ubicación (presencial/virtual): ").strip()
    participantes = input("Participantes (separados por comas): ").strip()
    notas = input("Notas: ").strip()
    
    # Opcional: asociar a candidato/vacante
    cid = input("ID candidato (opcional): ").strip() or None
    vid = input("ID vacante (opcional): ").strip() or None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calendario (titulo, tipo, fecha_hora, duracion, ubicacion, participantes, notas, candidato_id, vacante_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, tipo, fecha_hora, duracion, ubicacion, participantes, notas, cid, vid))
    conn.commit()
    conn.close()
    
    print("\n✅ Cita programada correctamente.")
    pausa()


def listar_citas_proximas():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 CITAS PRÓXIMAS (hoy + 7 días)")
    print("=" * 70)
    
    hoy = datetime.now().strftime("%Y-%m-%d")
    fin_semana = (datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, titulo, tipo, fecha_hora, duracion, ubicacion, participantes 
        FROM calendario 
        WHERE fecha_hora BETWEEN ? AND ?
        ORDER BY fecha_hora ASC
    ''', (hoy, fin_semana))
    citas = cursor.fetchall()
    conn.close()
    
    if not citas:
        print("\n📭 No hay citas programadas en los próximos 7 días.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(citas)} citas\n")
    for c in citas:
        print(f"[{c[0]}] {c[1]} ({c[2]})")
        print(f"   📅 {c[3]} | ⏱️  {c[4]} min")
        if c[5]:
            print(f"   📍 {c[5]}")
        if c[6]:
            print(f"   👥 {c[6]}")
        print()
    
    pausa()


def modulo_onboarding():
    limpiar_pantalla()
    print("=" * 70)
    print("   🚀 PROCESO DE ONBOARDING")
    print("=" * 70)
    print("\n💡 Checklist automático al contratar:")
    print("   ☐ Notificar a RRHH (contrato, documentación)")
    print("   ☐ Notificar a Sistemas (cuenta email, laptop, accesos)")
    print("   ☐ Notificar a Departamento (espacio, equipo, mentor)")
    print("   ☐ Preparar bienvenida primer día")
    print("   ☐ Plan formación primer mes")
    print("\n1. ➕ Iniciar nuevo proceso de onboarding")
    print("2. 📋 Listar procesos pendientes")
    print("0. ⬅️  Volver")
    
    opcion = input("\n➤ Opción: ").strip()
    
    if opcion == "1":
        iniciar_onboarding()
    elif opcion == "2":
        listar_onboarding_pendiente()


def iniciar_onboarding():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ INICIAR PROCESO DE ONBOARDING")
    print("=" * 70)
    
    cid = input("\nID del candidato seleccionado*: ").strip()
    while not cid:
        print("⚠️  El ID es obligatorio")
        cid = input("ID del candidato seleccionado*: ").strip()
    
    # Verificar candidato existe y está seleccionado
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM candidatos WHERE id = ? AND estado IN ("offer", "contratado")', (cid,))
    candidato = cursor.fetchone()
    
    if not candidato:
        conn.close()
        print("\n⚠️  Candidato no encontrado o no en estado válido para onboarding.")
        pausa()
        return
    
    fecha_inicio = input(f"Fecha de inicio (YYYY-MM-DD)*: ").strip()
    while True:
        try:
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️  Formato no válido. Ejemplo: 2026-03-01")
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD)*: ").strip()
    
    tutor = input("Tutor/mentor en el equipo: ").strip()
    
    # Crear registro onboarding
    cursor.execute('''
        INSERT INTO onboarding (candidato_id, fecha_inicio, tutor_empresa, estado)
        VALUES (?, ?, ?, 'pendiente')
    ''', (cid, fecha_inicio, tutor))
    
    # Actualizar estado candidato
    cursor.execute('UPDATE candidatos SET estado = "contratado" WHERE id = ?', (cid,))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Proceso de onboarding iniciado para: {candidato[0]}")
    print(f"   Fecha inicio: {fecha_inicio}")
    print(f"   Tutor asignado: {tutor or 'Pendiente'}")
    pausa()


def listar_onboarding_pendiente():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 PROCESOS DE ONBOARDING PENDIENTES")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.id, c.nombre, o.fecha_inicio, o.tutor_empresa, o.estado
        FROM onboarding o
        JOIN candidatos c ON o.candidato_id = c.id
        WHERE o.estado = 'pendiente'
        ORDER BY o.fecha_inicio ASC
    ''')
    procesos = cursor.fetchall()
    conn.close()
    
    if not procesos:
        print("\n📭 No hay procesos de onboarding pendientes.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(procesos)} procesos pendientes\n")
    for p in procesos:
        print(f"[{p[0]}] {p[1]}")
        print(f"   📅 Inicio: {p[2]} | 👔 Tutor: {p[3] or 'Sin asignar'} | 🏷️  Estado: {p[4]}")
        print("   Checklist:")
        print("     ☐ RRHH notificado")
        print("     ☐ Sistemas notificado")
        print("     ☐ Departamento notificado")
        print()
    
    pausa()


def modulo_anotaciones():
    limpiar_pantalla()
    print("=" * 70)
    print("   📝 ANOTACIONES PROPIAS")
    print("=" * 70)
    print("\n💡 Espacio privado para notas personales:")
    print("   • Reflexiones post-entrevista")
    print("   • Ideas para mejorar procesos RRHH")
    print("   • Recordatorios internos")
    print("\n1. ➕ Nueva anotación")
    print("2. 📋 Listar anotaciones")
    print("0. ⬅️  Volver")
    
    opcion = input("\n➤ Opción: ").strip()
    
    if opcion == "1":
        crear_anotacion()
    elif opcion == "2":
        listar_anotaciones()


def crear_anotacion():
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ NUEVA ANOTACIÓN")
    print("=" * 70)
    
    titulo = input("\nTítulo (opcional): ").strip()
    contenido = input("Contenido*: ").strip()
    while not contenido:
        print("⚠️  El contenido no puede estar vacío")
        contenido = input("Contenido*: ").strip()
    
    categoria = input("Categoría (ej: candidatos, procesos, ideas): ").strip()
    
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO anotaciones (titulo, contenido, categoria, fecha_creacion, ultima_modificacion)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, contenido, categoria, ahora, ahora))
    conn.commit()
    conn.close()
    
    print("\n✅ Anotación guardada correctamente.")
    pausa()


def listar_anotaciones():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 MIS ANOTACIONES")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, categoria, fecha_creacion FROM anotaciones ORDER BY fecha_creacion DESC')
    anotaciones = cursor.fetchall()
    conn.close()
    
    if not anotaciones:
        print("\n📭 No hay anotaciones guardadas.")
        pausa()
        return
    
    print(f"\n📊 Total: {len(anotaciones)} anotaciones\n")
    for a in anotaciones:
        titulo = a[1] if a[1] else "(Sin título)"
        cat = f"[{a[2]}]" if a[2] else ""
        print(f"[{a[0]}] {titulo} {cat}")
        print(f"   📅 {a[3]}")
        print()
    
    ver_detalle = input("¿Ver detalle de alguna anotación? (ID o Enter para salir): ").strip()
    if ver_detalle:
        ver_anotacion_detalle(ver_detalle)


def ver_anotacion_detalle(anotacion_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT titulo, contenido, categoria, fecha_creacion, ultima_modificacion FROM anotaciones WHERE id = ?', (anotacion_id,))
    anotacion = cursor.fetchone()
    conn.close()
    
    if not anotacion:
        print("\n⚠️  Anotación no encontrada.")
        pausa()
        return
    
    limpiar_pantalla()
    print("=" * 70)
    print("   📝 DETALLE DE ANOTACIÓN")
    print("=" * 70)
    print(f"\nTítulo: {anotacion[0] or '(Sin título)'}")
    if anotacion[2]:
        print(f"Categoría: {anotacion[2]}")
    print(f"📅 Creada: {anotacion[3]}")
    print(f"✏️  Última modificación: {anotacion[4]}")
    print(f"\nContenido:\n{anotacion[1]}")
    pausa()


def modulo_glosario():
    limpiar_pantalla()
    print("=" * 70)
    print("   📖 GLOSARIO DE TÉRMINOS")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT categoria FROM glosario ORDER BY categoria')
    categorias = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print("\nCategorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        print(f"  {i}. {cat.capitalize()}")
    print("  0. Todas")
    
    opcion = input("\n➤ Selecciona categoría (número) o 0 para todas: ").strip().lower()
    
    if opcion == "0" or not opcion:
        categoria_sel = None
    else:
        try:
            idx = int(opcion) - 1
            categoria_sel = categorias[idx]
        except (ValueError, IndexError):
            categoria_sel = None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if categoria_sel:
        cursor.execute('SELECT * FROM glosario WHERE categoria = ? ORDER BY termino', (categoria_sel,))
    else:
        cursor.execute('SELECT * FROM glosario ORDER BY categoria, termino')
    
    terminos = cursor.fetchall()
    conn.close()
    
    if not terminos:
        print("\n📭 No hay términos con esos criterios.")
        pausa()
        return
    
    categoria_actual = None
    for g in terminos:
        if g[3] != categoria_actual:
            categoria_actual = g[3]
            print(f"\n{'='*70}")
            print(f"📌 CATEGORÍA: {categoria_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {g[1]}")
        print(f"   {g[2]}")
    
    pausa()


# ========================================
# MENÚ PRINCIPAL (20 módulos completos)
# ========================================

def menu_principal():
    inicializar_db()
    
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📋 APLICACIÓN INTEGRAL DE SELECCIÓN Y RECLUTAMIENTO")
        print("=" * 70)
        print("\n1. 👥 Base de datos de candidatos (+ CVs)")
        print("2. 💼 Selección de la empresa (vacantes)")
        print("3. 📊 Evaluaciones R/S/T (scoring automático)")
        print("4. ❓ Banco de preguntas de entrevista")
        print("5. 👤 Perfiles seleccionados por la empresa")
        print("6. 🏢 Presentación de empresa")
        print("7. 🚀 Metodologías ágiles")
        print("8. 📋 Convenio oficinas Madrid")
        print("9. 📜 Estatuto de los trabajadores")
        print("10. ♿ Asociaciones colaboración")
        print("11. 🎓 Centros de estudios y prácticas")
        print("12. 👨‍🎓 Estudiantes de prácticas")
        print("13. 💼 Portales de empleo")
        print("14. 📄 Plantillas vacantes")
        print("15. 🤝 Team building")
        print("16. 📜 Normativa interna")
        print("17. ✅ Tareas, objetivos y alarmas")
        print("18. 📅 Calendario y automatización")
        print("19. 🚀 Proceso de onboarding")
        print("20. 📝 Anotaciones propias")
        print("21. 📖 Glosario de términos")
        print("0. ❌ Salir")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-21): ").strip()
        
        if opcion == "1":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   👥 BASE DE DATOS DE CANDIDATOS")
                print("=" * 70)
                print("\n1. 🆕 Registrar nuevo candidato (+ CV)")
                print("2. 🔍 Buscar/Listar candidatos")
                print("3. 👁️  Ver detalle de candidato")
                print("4. 📥 Descargar/ver CV")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_candidato()
                elif subopcion == "2":
                    listar_candidatos()
                elif subopcion == "3":
                    ver_detalle_candidato()
                elif subopcion == "4":
                    descargar_cv()
                elif subopcion == "0":
                    break
        
        elif opcion == "2":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   💼 SELECCIÓN DE LA EMPRESA - VACANTES")
                print("=" * 70)
                print("\n1. ➕ Crear nueva vacante")
                print("2. 📋 Listar vacantes")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_vacante()
                elif subopcion == "2":
                    listar_vacantes()
                elif subopcion == "0":
                    break
        
        elif opcion == "3":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   📊 EVALUACIONES R/S/T - Scoring Automático")
                print("=" * 70)
                print("\n1. ➕ Nueva evaluación")
                print("2. 📋 Ver historial evaluaciones")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_evaluacion()
                elif subopcion == "2":
                    ver_historial_evaluaciones()
                elif subopcion == "0":
                    break
        
        elif opcion == "4":
            modulo_preguntas()
        elif opcion == "5":
            modulo_perfiles_empresa()
        elif opcion == "6":
            modulo_presentacion_empresa()
        elif opcion == "7":
            modulo_metodologias_agiles()
        elif opcion == "8":
            modulo_convenio_madrid()
        elif opcion == "9":
            modulo_estatuto_trabajadores()
        elif opcion == "10":
            modulo_asociaciones()
        elif opcion == "11":
            modulo_centros_formacion()
        elif opcion == "12":
            modulo_estudiantes_practicas()
        elif opcion == "13":
            modulo_portales_empleo()
        elif opcion == "14":
            modulo_plantillas_vacantes()
        elif opcion == "15":
            modulo_team_building()
        elif opcion == "16":
            modulo_normativa_interna()
        elif opcion == "17":
            modulo_tareas()
        elif opcion == "18":
            modulo_calendario()
        elif opcion == "19":
            modulo_onboarding()
        elif opcion == "20":
            modulo_anotaciones()
        elif opcion == "21":
            modulo_glosario()
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto!")
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def ver_historial_evaluaciones():
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 HISTORIAL DE EVALUACIONES R/S/T")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT nombre FROM candidatos WHERE id = ?', (cid,))
    candidato = cursor.fetchone()
    
    if not candidato:
        conn.close()
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    cursor.execute('''
        SELECT * FROM evaluaciones 
        WHERE candidato_id = ? 
        ORDER BY fecha DESC
    ''', (cid,))
    evaluaciones = cursor.fetchall()
    conn.close()
    
    if not evaluaciones:
        print(f"\n📭 {candidato['nombre']} no tiene evaluaciones registradas.")
        pausa()
        return
    
    print(f"\n📊 Evaluaciones de {candidato['nombre']}: {len(evaluaciones)}\n")
    
    for e in evaluaciones:
        print(f"[{e['fecha']}] Evaluador: {e['evaluador']}")
        print(f"   R (Comunicación): {e['r_puntuacion']}/10 | {e['r_notas'] or '-'}")
        print(f"   S (Técnica):      {e['s_puntuacion']}/10 | {e['s_notas'] or '-'}")
        print(f"   T (Cultural):     {e['t_puntuacion']}/10 | {e['t_notas'] or '-'}")
        print(f"   ➤ Score final:    {e['score_final']:.2f}/10 | Recomendación: {e['recomendacion']}")
        if e['senales_encaje']:
            print(f"   ✅ {e['senales_encaje']}")
        print("-" * 70)
    
    pausa()


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    # Crear carpetas necesarias
    APP_DIR.mkdir(exist_ok=True)
    CVS_DIR.mkdir(exist_ok=True)
    
    # Mostrar información inicial
    limpiar_pantalla()
    print("=" * 70)
    print("   🚀 APLICACIÓN INTEGRAL DE SELECCIÓN Y RECLUTAMIENTO")
    print("=" * 70)
    print("\n✅ Carpeta de datos creada en:")
    print(f"   {APP_DIR.absolute()}")
    print("\n✅ Carpeta de CVs creada en:")
    print(f"   {CVS_DIR.absolute()}")
    print("\n💡 Características clave:")
    print("   • Scoring R/S/T automático con ponderación por perfil IT")
    print("   • Banco de preguntas especializado por perfil (Backend, DevOps, QA...)")
    print("   • Perfiles empresa con stack TM Forum/ODA real")
    print("   • Almacenamiento real de CVs (PDF/DOC/DOCX)")
    print("   • Checklist de 'señales de buen encaje' por perfil")
    print("   • 20 módulos completos listos para usar")
    print("   • Sin nombre asignado (solo 'Aplicación Integral de Selección')")
    print("   • Sin referencias a Alvatross fuera del módulo de presentación")
    pausa()
    
    # Ejecutar menú principal
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        pausa()
