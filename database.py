#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py
Gestor de base de datos SQLite para aplicación RRHH integral
Tablas: candidatos, vacantes, preguntas, perfiles_empresa, asociaciones,
        centros_practicas, portales_empleo, plantillas_vacantes,
        team_building, glosario
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """Gestor completo de la base de datos RRHH"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            self.db_path = Path("data") / "rrhh_app.db"
        else:
            self.db_path = Path(db_path)
        
        # Crear carpeta data si no existe
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Inicializar esquema de base de datos
        self._crear_esquema()
        self._sembrar_datos_iniciales()
    
    # ========================================
    # INICIALIZACIÓN Y ESQUEMA
    # ========================================
    
    def _crear_esquema(self):
        """Crear todas las tablas si no existen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla candidatos
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
        
        # Tabla preguntas entrevista
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
        
        # Tabla perfiles empresa
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
        
        # Tabla centros prácticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS centros_practicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT,
                contacto TEXT,
                web TEXT,
                convenio_activo BOOLEAN DEFAULT 0
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
        
        # Tabla glosario
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
    
    def _sembrar_datos_iniciales(self):
        """Sembrar datos iniciales si las tablas están vacías"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Preguntas iniciales
        cursor.execute('SELECT COUNT(*) FROM preguntas')
        if cursor.fetchone()[0] == 0:
            preguntas = [
                ('general', None, 'Cuéntame tu trayectoria profesional en los últimos 5 años', 'medio', 'trayectoria,experiencia'),
                ('general', None, '¿Por qué estás interesado en esta oportunidad?', 'medio', 'motivación'),
                ('tecnica', 'backend', '¿Cómo gestionarías la resiliencia ante fallos de dependencias externas en un microservicio?', 'dificil', 'resiliencia,microservicios'),
                ('tecnica', 'devops', '¿Cómo diseñarías un pipeline CI/CD con controles de seguridad integrados?', 'dificil', 'cicd,seguridad'),
                ('cultural', None, 'Describe tu experiencia trabajando en equipos multidisciplinares', 'medio', 'colaboración,equipos'),
                ('situacional', None, 'Un bug crítico llega a producción. ¿Cuál es tu protocolo de actuación?', 'dificil', 'crisis,producción')
            ]
            cursor.executemany('''
                INSERT INTO preguntas (categoria, subcategoria, texto, nivel_dificultad, tags)
                VALUES (?, ?, ?, ?, ?)
            ''', preguntas)
        
        # Perfiles empresa iniciales
        cursor.execute('SELECT COUNT(*) FROM perfiles_empresa')
        if cursor.fetchone()[0] == 0:
            perfiles = [
                ('Backend Developer', 'Desarrollo de microservicios y APIs REST', 'Java, Spring Boot, PostgreSQL, Kubernetes', 'Desarrollo módulos OSS, APIs, integración sistemas', 'mid', 35000, 50000),
                ('DevOps Engineer', 'Automatización de despliegues y operaciones', 'Docker, Kubernetes, AWS/Azure, Terraform, GitLab CI', 'Pipelines CI/CD, infraestructura cloud, monitorización', 'mid', 40000, 55000),
                ('QA Automation Engineer', 'Aseguramiento de calidad mediante pruebas automatizadas', 'Selenium, Cypress, JUnit, Postman, Jenkins', 'Diseño planes prueba, automatización APIs, colaboración con devs', 'mid', 32000, 45000)
            ]
            cursor.executemany('''
                INSERT INTO perfiles_empresa (nombre, descripcion, stack, responsabilidades, seniority, salario_min, salario_max)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', perfiles)
        
        # Asociaciones iniciales
        cursor.execute('SELECT COUNT(*) FROM asociaciones')
        if cursor.fetchone()[0] == 0:
            asociaciones = [
                ('Inserta', 'discapacidad', 'info@inserta.es', 'https://www.inserta.es', 'Fundación ONCE para inserción laboral personas con discapacidad'),
                ('Fundación Adecco', 'discapacidad', 'info@fundacionadecco.es', 'https://www.fundacionadecco.es', 'Inserción laboral colectivos vulnerables'),
                ('Mujeres Tech', 'mujeres', 'contacto@mujerestech.es', 'https://mujerestech.es', 'Comunidad mujeres en tecnología'),
                ('AdaLab', 'mujeres', 'hola@adalab.es', 'https://adalab.es', 'Formación tecnológica para mujeres')
            ]
            cursor.executemany('''
                INSERT INTO asociaciones (nombre, tipo, contacto, web, notas)
                VALUES (?, ?, ?, ?, ?)
            ''', asociaciones)
        
        # Portales empleo iniciales
        cursor.execute('SELECT COUNT(*) FROM portales_empleo')
        if cursor.fetchone()[0] == 0:
            portales = [
                ('LinkedIn Jobs', 'https://linkedin.com/jobs', 'general', 'Premium Recruiter', 'Alta visibilidad IT'),
                ('InfoJobs', 'https://www.infojobs.net', 'general', 'Bolsa completa', 'Alto volumen candidatos España'),
                ('Tecnoempleo', 'https://www.tecnoempleo.com', 'IT', 'Gratuito/Pro', 'Especializado IT/Telecom'),
                ('Stack Overflow Jobs', 'https://stackoverflow.com/jobs', 'IT', 'Gratuito', 'Talento técnico senior'),
                ('GitHub Jobs', 'https://jobs.github.com', 'IT', 'Gratuito', 'Desarrolladores open source')
            ]
            cursor.executemany('''
                INSERT INTO portales_empleo (nombre, url, tipo, coste, notas)
                VALUES (?, ?, ?, ?, ?)
            ''', portales)
        
        # Team building iniciales
        cursor.execute('SELECT COUNT(*) FROM team_building')
        if cursor.fetchone()[0] == 0:
            actividades = [
                ('deporte', 'Escape Room Tecnológico', 'EscapeKings', '25€/persona', '2 horas', 4, 8, 'Resolución problemas en equipo con temática ciberseguridad'),
                ('gastronomia', 'Taller de cocina colaborativa', 'Cook&Team', '45€/persona', '3 horas', 6, 20, 'Elaboración menú completo en equipos rotativos'),
                ('naturaleza', 'Ruta senderismo + picnic', 'AireLibre', '15€/persona', '5 horas', 10, 30, 'Ruta guiada por Sierra de Guadarrama'),
                ('cultura', 'Visita guiada Museo Reina Sofía + taller', 'ArteEnEquipo', '20€/persona', '4 horas', 8, 25, 'Recorrido obras + taller creatividad'),
                ('solidaridad', 'Voluntariado huerto urbano', 'HuertosSolidarios', 'Donación', '3 horas', 5, 15, 'Mantenimiento huerto para comedores sociales')
            ]
            cursor.executemany('''
                INSERT INTO team_building (categoria, nombre_actividad, empresa_proveedora, precio_estimado, duracion, participantes_min, participantes_max, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', actividades)
        
        # Glosario inicial
        cursor.execute('SELECT COUNT(*) FROM glosario')
        if cursor.fetchone()[0] == 0:
            terminos = [
                ('API', 'Application Programming Interface: interfaz que permite la comunicación entre sistemas', 'técnico'),
                ('DevOps', 'Cultura y conjunto de prácticas que unen desarrollo y operaciones para acelerar entregas', 'metodologia'),
                ('GDPR', 'Reglamento General de Protección de Datos de la UE. Marco legal para tratamiento datos personales', 'legal'),
                ('Kanban', 'Método ágil de gestión visual del trabajo con límites WIP (Work In Progress)', 'metodologia'),
                ('Microservicios', 'Arquitectura de software donde una aplicación se estructura como conjunto de servicios pequeños e independientes', 'técnico'),
                ('ODA', 'Open Digital Architecture: marco de referencia para arquitecturas digitales abiertas', 'telecom'),
                ('OSS', 'Operational Support Systems: sistemas que gestionan operaciones de red y servicios en telecomunicaciones', 'telecom'),
                ('Scrum', 'Framework ágil con sprints, roles definidos (PO, SM, Dev Team) y ceremonias estructuradas', 'metodologia'),
                ('SLA', 'Service Level Agreement: acuerdo de nivel de servicio que define expectativas entre proveedor y cliente', 'legal'),
                ('Time to Hire', 'Métrica RRHH: tiempo transcurrido desde apertura vacante hasta aceptación oferta', 'rrhh')
            ]
            cursor.executemany('''
                INSERT INTO glosario (termino, definicion, categoria)
                VALUES (?, ?, ?)
            ''', terminos)
        
        conn.commit()
        conn.close()
    
    # ========================================
    # CRUD CANDIDATOS
    # ========================================
    
    def crear_candidato(self, datos: Dict) -> str:
        """Crear nuevo candidato. Devuelve ID generado."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        cursor.execute('''
            INSERT INTO candidatos (
                id, nombre, email, telefono, linkedin, github, localizacion,
                remoto, disponibilidad, nivel_estudios, titulacion, certificaciones,
                idiomas, experiencia_total, experiencia_telecom,
                stack_lenguajes, stack_frameworks, stack_bbdd, stack_cloud,
                stack_devops, stack_apis, competencias, salario_esperado,
                estado, perfil_it, seniority, gdpr_consent, fecha_registro,
                origen, notas
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
            datos.get('gdpr_consent', 0),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos.get('origen', 'manual'),
            datos.get('notas', '')
        ))
        
        conn.commit()
        conn.close()
        return candidato_id
    
    def obtener_candidato(self, candidato_id: str) -> Optional[Dict]:
        """Obtener candidato por ID. Devuelve None si no existe."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM candidatos WHERE id = ?', (candidato_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def listar_candidatos(self, buscar: str = None, estado: str = None, 
                         perfil_it: str = None) -> List[Dict]:
        """Listar candidatos con filtros opcionales."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT id, nombre, email, telefono, stack_lenguajes, perfil_it, seniority, estado, fecha_registro FROM candidatos WHERE estado != 'archivado'"
        params = []
        
        if estado:
            query += " AND estado = ?"
            params.append(estado)
        
        if perfil_it:
            query += " AND perfil_it = ?"
            params.append(perfil_it)
        
        if buscar:
            query += " AND (nombre LIKE ? OR stack_lenguajes LIKE ? OR email LIKE ?)"
            buscar_param = f"%{buscar}%"
            params.extend([buscar_param, buscar_param, buscar_param])
        
        query += " ORDER BY fecha_registro DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def actualizar_candidato(self, candidato_id: str, datos: Dict) -> bool:
        """Actualizar campos de un candidato. Devuelve True si exitoso."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        campos = []
        valores = []
        for campo, valor in datos.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(candidato_id)
        query = f"UPDATE candidatos SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(query, valores)
        exito = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return exito
    
    def archivar_candidato(self, candidato_id: str) -> bool:
        """Archivar candidato (no borrar físicamente)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE candidatos SET estado = "archivado" WHERE id = ?', (candidato_id,))
        exito = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return exito
    
    # ========================================
    # CRUD VACANTES
    # ========================================
    
    def crear_vacante(self, datos: Dict) -> str:
        """Crear nueva vacante. Devuelve ID generado."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generar ID único VAC-YYYY-NNN
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
    
    def obtener_vacante(self, vacante_id: str) -> Optional[Dict]:
        """Obtener vacante por ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vacantes WHERE id = ?', (vacante_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def listar_vacantes(self, estado: str = None, departamento: str = None) -> List[Dict]:
        """Listar vacantes con filtros."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM vacantes"
        params = []
        
        condiciones = []
        if estado:
            condiciones.append("estado = ?")
            params.append(estado)
        if departamento:
            condiciones.append("departamento = ?")
            params.append(departamento)
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY fecha_apertura DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def actualizar_vacante(self, vacante_id: str, datos: Dict) -> bool:
        """Actualizar vacante."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        campos = []
        valores = []
        for campo, valor in datos.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(vacante_id)
        query = f"UPDATE vacantes SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(query, valores)
        exito = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return exito
    
    # ========================================
    # CRUD PREGUNTAS
    # ========================================
    
    def listar_preguntas(self, categoria: str = None, subcategoria: str = None, 
                        buscar: str = None) -> List[Dict]:
        """Listar preguntas con filtros."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM preguntas"
        params = []
        
        condiciones = []
        if categoria:
            condiciones.append("categoria = ?")
            params.append(categoria)
        if subcategoria:
            condiciones.append("subcategoria = ?")
            params.append(subcategoria)
        if buscar:
            condiciones.append("(texto LIKE ? OR tags LIKE ?)")
            buscar_param = f"%{buscar}%"
            params.extend([buscar_param, buscar_param])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY categoria, subcategoria, nivel_dificultad DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def crear_pregunta(self, categoria: str, texto: str, subcategoria: str = None,
                      nivel_dificultad: str = 'medio', tags: str = None) -> int:
        """Crear nueva pregunta. Devuelve ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO preguntas (categoria, subcategoria, texto, nivel_dificultad, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (categoria, subcategoria, texto, nivel_dificultad, tags))
        
        pregunta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pregunta_id
    
    # ========================================
    # CRUD PERFILES EMPRESA
    # ========================================
    
    def listar_perfiles_empresa(self) -> List[Dict]:
        """Listar todos los perfiles definidos por la empresa."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM perfiles_empresa ORDER BY seniority, nombre')
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    # ========================================
    # CRUD ASOCIACIONES
    # ========================================
    
    def listar_asociaciones(self, tipo: str = None) -> List[Dict]:
        """Listar asociaciones con filtro opcional por tipo."""
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
    
    def crear_asociacion(self, nombre: str, tipo: str, contacto: str = None,
                        web: str = None, notas: str = None) -> int:
        """Crear nueva asociación."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO asociaciones (nombre, tipo, contacto, web, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, tipo, contacto, web, notas))
        
        asociacion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return asociacion_id
    
    # ========================================
    # CRUD PORTALES EMPLEO
    # ========================================
    
    def listar_portales_empleo(self) -> List[Dict]:
        """Listar todos los portales de empleo."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM portales_empleo ORDER BY tipo, nombre')
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    # ========================================
    # CRUD TEAM BUILDING
    # ========================================
    
    def listar_team_building(self, categoria: str = None) -> List[Dict]:
        """Listar actividades de team building."""
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
    
    def listar_categorias_team_building(self) -> List[str]:
        """Listar categorías únicas de team building."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categoria FROM team_building ORDER BY categoria')
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categorias
    
    # ========================================
    # CRUD GLOSARIO
    # ========================================
    
    def listar_glosario(self, categoria: str = None) -> List[Dict]:
        """Listar términos del glosario."""
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
    
    def listar_categorias_glosario(self) -> List[str]:
        """Listar categorías únicas del glosario."""
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
        """Devolver ruta absoluta de la base de datos."""
        return str(self.db_path.absolute())
    
    def exportar_csv(self, tabla: str, ruta_salida: str) -> bool:
        """Exportar cualquier tabla a CSV."""
        import csv
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SELECT * FROM {tabla}")
            columnas = [description[0] for description in cursor.description]
            filas = cursor.fetchall()
            
            with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columnas)
                writer.writerows(filas)
            
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error exportando {tabla}: {e}")
            return False
