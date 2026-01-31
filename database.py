#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py
Gestor de base de datos SQLite para aplicación RRHH integral
20 módulos: candidatos, vacantes, preguntas, perfiles, empresa, ágiles,
convenio, estatuto, asociaciones, centros, prácticas, portales, plantillas,
team building, normativa, tareas, calendario, onboarding, anotaciones, glosario
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import os
import shutil


class DatabaseManager:
    """Gestor completo de la base de datos RRHH"""
    
    def __init__(self, db_path: str = None, cv_folder: str = None):
        # Rutas
        self.db_path = Path(db_path) if db_path else Path("data") / "rrhh_app.db"
        self.cv_folder = Path(cv_folder) if cv_folder else Path("cvs")
        
        # Crear carpetas si no existen
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self.cv_folder.mkdir(exist_ok=True, parents=True)
        
        # Inicializar esquema y datos
        self._crear_esquema()
        self._sembrar_datos_iniciales()
    
    # ========================================
    # ESQUEMA DE BASE DE DATOS
    # ========================================
    
    def _crear_esquema(self):
        """Crear todas las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Candidatos
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
                stack_lenguajes TEXT,
                stack_frameworks TEXT,
                stack_bbdd TEXT,
                stack_cloud TEXT,
                stack_devops TEXT,
                stack_apis TEXT,
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
        
        # Vacantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacantes (
                id TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                departamento TEXT,
                ubicacion TEXT,
                modalidad TEXT,
                stack_obligatorio TEXT NOT NULL,
                stack_deseable TEXT,
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
        
        # Preguntas entrevista
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                subcategoria TEXT,
                texto TEXT NOT NULL,
                nivel_dificultad TEXT DEFAULT 'medio',
                tags TEXT
            )
        ''')
        
        # Perfiles empresa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles_empresa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                stack TEXT,
                responsabilidades TEXT,
                seniority TEXT,
                salario_min INTEGER,
                salario_max INTEGER
            )
        ''')
        
        # Asociaciones colaboración
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
        
        # Centros de formación
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS centros_formacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,  -- universidad | fp | negocio | colocacion
                contacto TEXT,
                web TEXT,
                direccion TEXT,
                convenio_activo BOOLEAN DEFAULT 0
            )
        ''')
        
        # Estudiantes prácticas
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
        
        # Portales empleo
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
        
        # Plantillas vacantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plantillas_vacantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                departamento TEXT,
                ultima_actualizacion TEXT
            )
        ''')
        
        # Team building
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
        
        # Normativa interna
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS normativa_interna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,  -- anticonrrupcion | discapacidad | lgtb | otro
                contenido TEXT NOT NULL,
                fecha_aprobacion TEXT,
                version TEXT
            )
        ''')
        
        # Tareas y alarmas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                tipo TEXT,  -- tarea | objetivo | alarma
                prioridad TEXT DEFAULT 'media',
                fecha_limite TEXT,
                responsable TEXT,
                estado TEXT DEFAULT 'pendiente',
                completado BOOLEAN DEFAULT 0,
                fecha_creacion TEXT NOT NULL,
                recordatorio BOOLEAN DEFAULT 0
            )
        ''')
        
        # Calendario y citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calendario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,  -- entrevista | reunion | otro
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
        
        # Onboarding
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
                checklist TEXT  -- JSON con pasos completados
            )
        ''')
        
        # Anotaciones propias
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
        
        # Glosario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS glosario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                termino TEXT NOT NULL UNIQUE,
                definicion TEXT NOT NULL,
                categoria TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========================================
    # DATOS INICIALES (sembrado)
    # ========================================
    
    def _sembrar_datos_iniciales(self):
        """Sembrar datos útiles para usar desde el primer momento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Perfiles empresa
        cursor.execute('SELECT COUNT(*) FROM perfiles_empresa')
        if cursor.fetchone()[0] == 0:
            perfiles = [
                ('Backend Developer', 'Desarrollo microservicios y APIs REST', 'Java, Spring Boot, PostgreSQL, Kubernetes', 'Desarrollo módulos OSS, APIs, integración sistemas', 'mid', 35000, 50000),
                ('DevOps Engineer', 'Automatización despliegues y operaciones', 'Docker, Kubernetes, AWS/Azure, Terraform, GitLab CI', 'Pipelines CI/CD, infraestructura cloud, monitorización', 'mid', 40000, 55000),
                ('QA Automation Engineer', 'Aseguramiento calidad mediante pruebas automatizadas', 'Selenium, Cypress, JUnit, Postman, Jenkins', 'Diseño planes prueba, automatización APIs, colaboración con devs', 'mid', 32000, 45000),
                ('Frontend Developer', 'Desarrollo interfaces usuario', 'Angular, React, TypeScript, HTML5, CSS3', 'Componentes UI, integración APIs REST, optimización rendimiento', 'mid', 33000, 48000),
                ('Integrations Specialist', 'Conexión plataforma con sistemas externos', 'REST, TM Forum APIs, Kafka, RabbitMQ', 'Desarrollo adaptadores, validación contratos, troubleshooting', 'mid', 36000, 52000)
            ]
            cursor.executemany('''
                INSERT INTO perfiles_empresa (nombre, descripcion, stack, responsabilidades, seniority, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', perfiles)
        
        # Asociaciones
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
        
        # Centros formación
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
        
        # Portales empleo
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
        
        # Team building
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
        
        # Normativa interna
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
        
        # Glosario
        cursor.execute('SELECT COUNT(*) FROM glosario')
        if cursor.fetchone()[0] == 0:
            terminos = [
                ('API', 'Application Programming Interface: interfaz comunicación entre sistemas', 'técnico'),
                ('DevOps', 'Cultura uniendo desarrollo y operaciones para acelerar entregas', 'metodologia'),
                ('GDPR', 'Reglamento General Protección Datos UE. Marco legal tratamiento datos personales', 'legal'),
                ('Kanban', 'Método ágil gestión visual trabajo con límites WIP', 'metodologia'),
                ('Microservicios', 'Arquitectura aplicación como conjunto servicios pequeños e independientes', 'técnico'),
                ('ODA', 'Open Digital Architecture: marco referencia arquitecturas digitales abiertas', 'telecom'),
                ('OSS', 'Operational Support Systems: sistemas gestión operaciones red y servicios telecom', 'telecom'),
                ('Scrum', 'Framework ágil con sprints, roles definidos y ceremonias estructuradas', 'metodologia'),
                ('SLA', 'Service Level Agreement: acuerdo nivel servicio entre proveedor y cliente', 'legal'),
                ('Time to Hire', 'Métrica RRHH: tiempo desde apertura vacante hasta aceptación oferta', 'rrhh')
            ]
            cursor.executemany('''
                INSERT INTO glosario (termino, definicion, categoria)
                VALUES (?, ?, ?)
            ''', terminos)
        
        # Preguntas iniciales
        cursor.execute('SELECT COUNT(*) FROM preguntas')
        if cursor.fetchone()[0] == 0:
            preguntas = [
                ('general', None, 'Cuéntame tu trayectoria profesional últimos 5 años', 'medio', 'trayectoria,experiencia'),
                ('general', None, '¿Por qué estás interesado en esta oportunidad?', 'medio', 'motivacion'),
                ('tecnica', 'backend', '¿Cómo gestionarías resiliencia ante fallos dependencias externas en microservicio?', 'dificil', 'resiliencia,microservicios'),
                ('tecnica', 'devops', '¿Cómo diseñarías pipeline CI/CD con controles seguridad integrados?', 'dificil', 'cicd,seguridad'),
                ('cultural', None, 'Describe experiencia trabajando en equipos multidisciplinares', 'medio', 'colaboracion,equipos'),
                ('situacional', None, 'Bug crítico llega producción. ¿Protocolo actuación?', 'dificil', 'crisis,produccion')
            ]
            cursor.executemany('''
                INSERT INTO preguntas (categoria, subcategoria, texto, nivel_dificultad, tags)
                VALUES (?, ?, ?, ?, ?)
            ''', preguntas)
        
        conn.commit()
        conn.close()
    
    # ========================================
    # CRUD CANDIDATOS (con gestión de CVs)
    # ========================================
    
    def crear_candidato(self, datos: dict) -> str:
        """Crear candidato y guardar CV si existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
        cv_filename = None
        
        # Guardar CV si existe
        if datos.get('cv_data') and datos.get('cv_filename'):
            cv_filename = f"{candidato_id}_{datos['cv_filename']}"
            cv_path = self.cv_folder / cv_filename
            
            try:
                with open(cv_path, 'wb') as f:
                    f.write(datos['cv_data'])
            except Exception as e:
                print(f"⚠️  Error guardando CV: {e}")
                cv_filename = None
        
        cursor.execute('''
            INSERT INTO candidatos (
                id, nombre, email, telefono, linkedin, github, localizacion,
                remoto, disponibilidad, nivel_estudios, titulacion, certificaciones,
                idiomas, experiencia_total, experiencia_telecom,
                stack_lenguajes, stack_frameworks, stack_bbdd, stack_cloud,
                stack_devops, stack_apis, competencias, salario_esperado,
                estado, perfil_it, seniority, cv_filename, gdpr_consent,
                fecha_registro, origen, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidato_id,
            datos.get('nombre'),
            datos.get('email'),
            datos.get('telefono'),
            datos.get('linkedin'),
            datos.get('github'),
            datos.get('localizacion'),
            datos.get('remoto'),
            datos.get('disponibilidad'),
            datos.get('nivel_estudios'),
            datos.get('titulacion'),
            datos.get('certificaciones'),
            datos.get('idiomas'),
            datos.get('experiencia_total', 0),
            datos.get('experiencia_telecom', 0),
            datos.get('stack_lenguajes'),
            datos.get('stack_frameworks'),
            datos.get('stack_bbdd'),
            datos.get('stack_cloud'),
            datos.get('stack_devops'),
            datos.get('stack_apis'),
            datos.get('competencias'),
            datos.get('salario_esperado'),
            'activo',
            datos.get('perfil_it'),
            datos.get('seniority'),
            cv_filename,
            datos.get('gdpr_consent', 0),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos.get('origen', 'manual'),
            datos.get('notas', '')
        ))
        
        conn.commit()
        conn.close()
        return candidato_id
    
    def obtener_candidato(self, candidato_id: str) -> dict:
        """Obtener candidato por ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidatos WHERE id = ?', (candidato_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def listar_candidatos(self, buscar: str = None, estado: str = None) -> list:
        """Listar candidatos con filtros"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT id, nombre, email, telefono, stack_lenguajes, perfil_it, seniority, estado FROM candidatos WHERE estado != 'archivado'"
        params = []
        
        if estado:
            query += " AND estado = ?"
            params.append(estado)
        
        if buscar:
            query += " AND (nombre LIKE ? OR stack_lenguajes LIKE ? OR email LIKE ?)"
            buscar_param = f"%{buscar}%"
            params.extend([buscar_param, buscar_param, buscar_param])
        
        query += " ORDER BY fecha_registro DESC"
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def obtener_ruta_cv(self, candidato_id: str) -> str:
        """Obtener ruta absoluta del CV de un candidato"""
        candidato = self.obtener_candidato(candidato_id)
        if candidato and candidato.get('cv_filename'):
            return str(self.cv_folder / candidato['cv_filename'])
        return None
    
    # ========================================
    # CRUD VACANTES
    # ========================================
    
    def crear_vacante(self, datos: dict) -> str:
        """Crear nueva vacante"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM vacantes WHERE id LIKE ?', (f"VAC-{datetime.now().year}%",))
        count = cursor.fetchone()[0] + 1
        vacante_id = f"VAC-{datetime.now().year}-{count:03d}"
        
        cursor.execute('''
            INSERT INTO vacantes (
                id, titulo, departamento, ubicacion, modalidad,
                stack_obligatorio, stack_deseable,
                rango_salarial_min, rango_salarial_max,
                responsable, urgencia, estado, fecha_apertura, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vacante_id,
            datos.get('titulo'),
            datos.get('departamento'),
            datos.get('ubicacion'),
            datos.get('modalidad'),
            datos.get('stack_obligatorio'),
            datos.get('stack_deseable'),
            datos.get('rango_salarial_min', 0),
            datos.get('rango_salarial_max', 0),
            datos.get('responsable'),
            datos.get('urgencia', 'media'),
            'abierta',
            datetime.now().strftime("%Y-%m-%d"),
            datos.get('notas', '')
        ))
        
        conn.commit()
        conn.close()
        return vacante_id
    
    def listar_vacantes(self, estado: str = None) -> list:
        """Listar vacantes"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if estado:
            cursor.execute('SELECT * FROM vacantes WHERE estado = ? ORDER BY fecha_apertura DESC', (estado,))
        else:
            cursor.execute('SELECT * FROM vacantes ORDER BY fecha_apertura DESC')
        
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    # ========================================
    # MÓDULOS ADICIONALES (métodos esenciales)
    # ========================================
    
    def listar_preguntas(self, categoria: str = None, buscar: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM preguntas"
        params = []
        
        condiciones = []
        if categoria:
            condiciones.append("categoria = ?")
            params.append(categoria)
        if buscar:
            condiciones.append("(texto LIKE ? OR tags LIKE ?)")
            params.extend([f"%{buscar}%", f"%{buscar}%"])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY categoria, nivel_dificultad DESC"
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_perfiles_empresa(self) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM perfiles_empresa ORDER BY seniority, nombre')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_asociaciones(self, tipo: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if tipo:
            cursor.execute('SELECT * FROM asociaciones WHERE tipo = ? ORDER BY nombre', (tipo,))
        else:
            cursor.execute('SELECT * FROM asociaciones ORDER BY tipo, nombre')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_centros_formacion(self, tipo: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if tipo:
            cursor.execute('SELECT * FROM centros_formacion WHERE tipo = ? ORDER BY nombre', (tipo,))
        else:
            cursor.execute('SELECT * FROM centros_formacion ORDER BY tipo, nombre')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_estudiantes_practicas(self, estado: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if estado:
            cursor.execute('SELECT * FROM estudiantes_practicas WHERE estado = ? ORDER BY fecha_inicio DESC', (estado,))
        else:
            cursor.execute('SELECT * FROM estudiantes_practicas ORDER BY fecha_inicio DESC')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_portales_empleo(self) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM portales_empleo ORDER BY tipo, nombre')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_team_building(self, categoria: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if categoria:
            cursor.execute('SELECT * FROM team_building WHERE categoria = ? ORDER BY nombre_actividad', (categoria,))
        else:
            cursor.execute('SELECT * FROM team_building ORDER BY categoria, nombre_actividad')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_categorias_team_building(self) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categoria FROM team_building ORDER BY categoria')
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categorias
    
    def listar_normativa_interna(self, tipo: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if tipo:
            cursor.execute('SELECT * FROM normativa_interna WHERE tipo = ? ORDER BY fecha_aprobacion DESC', (tipo,))
        else:
            cursor.execute('SELECT * FROM normativa_interna ORDER BY fecha_aprobacion DESC')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def crear_tarea(self, titulo: str, descripcion: str = None, tipo: str = 'tarea',
                   prioridad: str = 'media', fecha_limite: str = None, responsable: str = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, tipo, prioridad, fecha_limite, responsable, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, descripcion, tipo, prioridad, fecha_limite, responsable, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea_id
    
    def listar_tareas(self, estado: str = 'pendiente', responsable: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM tareas WHERE estado = ?"
        params = [estado]
        if responsable:
            query += " AND responsable = ?"
            params.append(responsable)
        query += " ORDER BY fecha_limite ASC NULLS LAST"
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def crear_cita(self, titulo: str, tipo: str, fecha_hora: str, duracion: int = 60,
                  ubicacion: str = None, participantes: str = None, notas: str = None,
                  candidato_id: str = None, vacante_id: str = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calendario (titulo, tipo, fecha_hora, duracion, ubicacion, participantes, notas, candidato_id, vacante_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, tipo, fecha_hora, duracion, ubicacion, participantes, notas, candidato_id, vacante_id))
        cita_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cita_id
    
    def listar_citas(self, fecha_desde: str = None, fecha_hasta: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM calendario"
        params = []
        if fecha_desde and fecha_hasta:
            query += " WHERE fecha_hora BETWEEN ? AND ?"
            params.extend([fecha_desde, fecha_hasta])
        query += " ORDER BY fecha_hora ASC"
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def crear_onboarding(self, candidato_id: str, fecha_inicio: str, tutor_empresa: str = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO onboarding (candidato_id, fecha_inicio, tutor_empresa, checklist)
            VALUES (?, ?, ?, ?)
        ''', (candidato_id, fecha_inicio, tutor_empresa, '{}'))
        onboarding_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return onboarding_id
    
    def listar_onboarding_pendiente(self) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM onboarding WHERE estado = "pendiente" ORDER BY fecha_inicio ASC')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def crear_anotacion(self, titulo: str, contenido: str, categoria: str = None) -> int:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO anotaciones (titulo, contenido, categoria, fecha_creacion, ultima_modificacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, contenido, categoria, ahora, ahora))
        anotacion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return anotacion_id
    
    def listar_anotaciones(self, categoria: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if categoria:
            cursor.execute('SELECT * FROM anotaciones WHERE categoria = ? ORDER BY fecha_creacion DESC', (categoria,))
        else:
            cursor.execute('SELECT * FROM anotaciones ORDER BY fecha_creacion DESC')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_glosario(self, categoria: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if categoria and categoria != 'todas':
            cursor.execute('SELECT * FROM glosario WHERE categoria = ? ORDER BY termino', (categoria,))
        else:
            cursor.execute('SELECT * FROM glosario ORDER BY categoria, termino')
        resultados = cursor.fetchall()
        conn.close()
        return [dict(row) for row in resultados]
    
    def listar_categorias_glosario(self) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categoria FROM glosario ORDER BY categoria')
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categorias
    
    # ========================================
    # UTILIDADES
    # ========================================
    
    def obtener_ruta_db(self) -> str:
        return str(self.db_path.absolute())
    
    def obtener_ruta_cvs(self) -> str:
        return str(self.cv_folder.absolute())
