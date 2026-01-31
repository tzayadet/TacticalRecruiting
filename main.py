#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App RRHH - Módulos esenciales para selección IT/Telecom
⚠️  Ejecuta este archivo único. Sin dependencias externas.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import os
import sys


# ========================================
# INICIALIZAR BASE DE DATOS
# ========================================

def inicializar_db():
    """Crear base de datos y todas las tablas necesarias"""
    db_path = Path("data") / "rrhh_app.db"
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
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
    
    # Sembrar preguntas iniciales
    cursor.execute('SELECT COUNT(*) FROM preguntas')
    if cursor.fetchone()[0] == 0:
        preguntas_iniciales = [
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
        ''', preguntas_iniciales)
    
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
    
    # Sembrar perfiles IT iniciales
    cursor.execute('SELECT COUNT(*) FROM perfiles_empresa')
    if cursor.fetchone()[0] == 0:
        perfiles_iniciales = [
            ('Backend Developer', 'Desarrollo de microservicios y APIs REST', 'Java, Spring Boot, PostgreSQL, Kubernetes', 'Desarrollo módulos OSS, APIs TM Forum, integración sistemas', 'mid', 35000, 50000),
            ('DevOps Engineer', 'Automatización de despliegues y operaciones', 'Docker, Kubernetes, AWS/Azure, Terraform, GitLab CI', 'Pipelines CI/CD, infraestructura cloud, monitorización', 'mid', 40000, 55000),
            ('QA Automation Engineer', 'Aseguramiento de calidad mediante pruebas automatizadas', 'Selenium, Cypress, JUnit, Postman, Jenkins', 'Diseño planes prueba, automatización APIs, colaboración con devs', 'mid', 32000, 45000)
        ]
        cursor.executemany('''
            INSERT INTO perfiles_empresa (nombre, descripcion, stack, responsabilidades, seniority, salario_min, salario_max)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', perfiles_iniciales)
    
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
    
    # Sembrar asociaciones iniciales
    cursor.execute('SELECT COUNT(*) FROM asociaciones')
    if cursor.fetchone()[0] == 0:
        asociaciones_iniciales = [
            ('Inserta', 'discapacidad', 'info@inserta.es', 'https://www.inserta.es', 'Fundación ONCE para inserción laboral personas con discapacidad'),
            ('Fundación Adecco', 'discapacidad', 'info@fundacionadecco.es', 'https://www.fundacionadecco.es', 'Inserción laboral colectivos vulnerables'),
            ('Mujeres Tech', 'mujeres', 'contacto@mujerestech.es', 'https://mujerestech.es', 'Comunidad mujeres en tecnología'),
            ('AdaLab', 'mujeres', 'hola@adalab.es', 'https://adalab.es', 'Formación tecnológica para mujeres')
        ]
        cursor.executemany('''
            INSERT INTO asociaciones (nombre, tipo, contacto, web, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', asociaciones_iniciales)
    
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
    
    # Sembrar portales iniciales
    cursor.execute('SELECT COUNT(*) FROM portales_empleo')
    if cursor.fetchone()[0] == 0:
        portales_iniciales = [
            ('LinkedIn Jobs', 'https://linkedin.com/jobs', 'general', 'Premium Recruiter', 'Alta visibilidad IT'),
            ('InfoJobs', 'https://www.infojobs.net', 'general', 'Bolsa completa', 'Alto volumen candidatos España'),
            ('Tecnoempleo', 'https://www.tecnoempleo.com', 'IT', 'Gratuito/Pro', 'Especializado IT/Telecom'),
            ('Stack Overflow Jobs', 'https://stackoverflow.com/jobs', 'IT', 'Gratuito', 'Talento técnico senior'),
            ('GitHub Jobs', 'https://jobs.github.com', 'IT', 'Gratuito', 'Desarrolladores open source')
        ]
        cursor.executemany('''
            INSERT INTO portales_empleo (nombre, url, tipo, coste, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', portales_iniciales)
    
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
    
    # Sembrar actividades iniciales
    cursor.execute('SELECT COUNT(*) FROM team_building')
    if cursor.fetchone()[0] == 0:
        actividades_iniciales = [
            ('deporte', 'Escape Room Tecnológico', 'EscapeKings', '25€/persona', '2 horas', 4, 8, 'Resolución problemas en equipo con temática ciberseguridad'),
            ('gastronomia', 'Taller de cocina colaborativa', 'Cook&Team', '45€/persona', '3 horas', 6, 20, 'Elaboración menú completo en equipos rotativos'),
            ('naturaleza', 'Ruta senderismo + picnic', 'AireLibre', '15€/persona', '5 horas', 10, 30, 'Ruta guiada por Sierra de Guadarrama'),
            ('cultura', 'Visita guiada Museo Reina Sofía + taller', 'ArteEnEquipo', '20€/persona', '4 horas', 8, 25, 'Recorrido obras + taller creatividad'),
            ('solidaridad', 'Voluntariado huerto urbano', 'HuertosSolidarios', 'Donación', '3 horas', 5, 15, 'Mantenimiento huerto para comedores sociales')
        ]
        cursor.executemany('''
            INSERT INTO team_building (categoria, nombre_actividad, empresa_proveedora, precio_estimado, duracion, participantes_min, participantes_max, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', actividades_iniciales)
    
    # Tabla glosario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glosario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            termino TEXT NOT NULL UNIQUE,
            definicion TEXT NOT NULL,
            categoria TEXT
        )
    ''')
    
    # Sembrar términos iniciales
    cursor.execute('SELECT COUNT(*) FROM glosario')
    if cursor.fetchone()[0] == 0:
        terminos_iniciales = [
            ('API', 'Application Programming Interface: interfaz que permite la comunicación entre sistemas', 'técnico'),
            ('DevOps', 'Cultura y conjunto de prácticas que unen desarrollo y operaciones para acelerar entregas', 'metodologia'),
            ('GDPR', 'Reglamento General de Protección de Datos de la UE. Marco legal para tratamiento datos personales', 'legal'),
            ('Kanban', 'Método ágil de gestión visual del trabajo con límites WIP (Work In Progress)', 'metodologia'),
            ('Microservicios', 'Arquitectura de software donde una aplicación se estructura como conjunto de servicios pequeños e independientes', 'técnico'),
            ('ODA', 'Open Digital Architecture: marco de referencia de TM Forum para arquitecturas digitales abiertas', 'telecom'),
            ('OSS', 'Operational Support Systems: sistemas que gestionan operaciones de red y servicios en telecomunicaciones', 'telecom'),
            ('Scrum', 'Framework ágil con sprints, roles definidos (PO, SM, Dev Team) y ceremonias estructuradas', 'metodologia'),
            ('SLA', 'Service Level Agreement: acuerdo de nivel de servicio que define expectativas entre proveedor y cliente', 'legal'),
            ('Time to Hire', 'Métrica RRHH: tiempo transcurrido desde apertura vacante hasta aceptación oferta', 'rrhh')
        ]
        cursor.executemany('''
            INSERT INTO glosario (termino, definicion, categoria)
            VALUES (?, ?, ?)
        ''', terminos_iniciales)
    
    conn.commit()
    conn.close()
    return db_path


# ========================================
# UTILIDADES DE INTERFAZ
# ========================================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    input("\n↲ Pulsa Enter para continuar...")


# ========================================
# MÓDULO 1: BASE DE DATOS CANDIDATOS
# ========================================

def modulo_candidatos(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   👥 BASE DE DATOS DE CANDIDATOS")
        print("=" * 70)
        print("\n1. 🆕 Registrar nuevo candidato")
        print("2. 🔍 Buscar/Listar candidatos")
        print("3. 👁️  Ver detalle de candidato")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            registrar_candidato(db_path)
        elif opcion == "2":
            listar_candidatos(db_path)
        elif opcion == "3":
            ver_detalle_candidato(db_path)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def registrar_candidato(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🆕 REGISTRAR NUEVO CANDIDATO")
    print("=" * 70)
    
    datos = {}
    while not datos.get('nombre'):
        datos['nombre'] = input("\nNombre completo*: ").strip()
        if not datos['nombre']:
            print("⚠️  El nombre es obligatorio")
    
    datos['email'] = input("Email: ").strip()
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
    
    datos['stack_lenguajes'] = input("Lenguajes (ej: Java, Python, TypeScript): ").strip()
    datos['stack_frameworks'] = input("Frameworks (ej: Spring Boot, Angular, React): ").strip()
    datos['stack_bbdd'] = input("Bases de datos: ").strip()
    datos['stack_cloud'] = input("Cloud (AWS/Azure/GCP): ").strip()
    datos['stack_devops'] = input("DevOps (Docker, Kubernetes...): ").strip()
    datos['stack_apis'] = input("APIs/Integración: ").strip()
    datos['competencias'] = input("Competencias blandas: ").strip()
    datos['salario_esperado'] = input("Expectativa salarial (k€): ").strip()
    
    print("\nPerfiles IT:")
    print("  backend | devops | qa | integrations | frontend | other")
    datos['perfil_it'] = input("\nPerfil IT: ").strip().lower()
    
    print("\nSeniority:")
    print("  junior | mid | senior | lead")
    datos['seniority'] = input("\nSeniority: ").strip().lower()
    
    datos['notas'] = input("\nNotas iniciales: ").strip()
    gdpr = input("\n✅ Consentimiento GDPR registrado? (S/n): ").strip().lower()
    datos['gdpr_consent'] = 1 if gdpr in ('', 's', 'si', 'yes') else 0
    
    # Guardar en BD
    conn = sqlite3.connect(db_path)
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
        datos['nombre'],
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
        datos['experiencia_total'],
        datos['experiencia_telecom'],
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
        datos['gdpr_consent'],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'manual',
        datos.get('notas', '')
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Candidato registrado correctamente")
    print(f"   ID: {candidato_id}")
    print(f"   Nombre: {datos['nombre']}")
    pausa()


def listar_candidatos(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 LISTAR CANDIDATOS")
    print("=" * 70)
    
    buscar = input("\nBuscar (nombre, stack, puesto) - Deja en blanco para todos: ").strip()
    estado = input("Filtrar por estado (activo/inactivo) - Deja en blanco: ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT id, nombre, email, telefono, stack_lenguajes, perfil_it, seniority, estado FROM candidatos WHERE estado != 'archivado'"
    params = []
    
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    
    if buscar:
        query += " AND (nombre LIKE ? OR stack_lenguajes LIKE ?)"
        buscar_param = f"%{buscar}%"
        params.extend([buscar_param, buscar_param])
    
    query += " ORDER BY fecha_registro DESC"
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No se encontraron candidatos.")
        pausa()
        return
    
    print(f"\n📊 Encontrados: {len(resultados)} candidatos\n")
    print(f"{'ID':<15} {'Nombre':<25} {'Email':<30} {'Perfil':<15} {'Seniority':<10}")
    print("-" * 95)
    
    for row in resultados:
        print(f"{row[0]:<15} {row[1][:23]:<25} {row[2][:28] if row[2] else '-':<30} "
              f"{row[5] or '-':<15} {row[6] or '-':<10}")
    
    pausa()


def ver_detalle_candidato(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  DETALLE DE CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(db_path)
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
    print(f"   Telecom:     {candidato['experiencia_telecom']} años")
    
    print(f"\n🛠️  Stack técnico:")
    print(f"   Lenguajes:   {candidato['stack_lenguajes'] or '-'}")
    print(f"   Frameworks:  {candidato['stack_frameworks'] or '-'}")
    print(f"   BBDD:        {candidato['stack_bbdd'] or '-'}")
    print(f"   Cloud:       {candidato['stack_cloud'] or '-'}")
    print(f"   DevOps:      {candidato['stack_devops'] or '-'}")
    print(f"   APIs:        {candidato['stack_apis'] or '-'}")
    
    print(f"\n🌟 Competencias: {candidato['competencias'] or '-'}")
    print(f"💰 Salario esperado: {candidato['salario_esperado'] or '-'}")
    print(f"👤 Perfil IT: {candidato['perfil_it'] or '-'}")
    print(f"⭐ Seniority: {candidato['seniority'] or '-'}")
    
    print(f"\n📝 Notas:")
    print(f"   {candidato['notas'] or '-'}")
    
    print(f"\n🛡️  GDPR: {'✅ Consentimiento registrado' if candidato['gdpr_consent'] else '⚠️  Pendiente'}")
    print(f"📅 Registro: {candidato['fecha_registro']}")
    
    conn.close()
    pausa()


# ========================================
# MÓDULO 2: SELECCIÓN DE LA EMPRESA (VACANTES)
# ========================================

def modulo_vacantes(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   💼 SELECCIÓN DE LA EMPRESA - VACANTES")
        print("=" * 70)
        print("\n1. ➕ Crear nueva vacante")
        print("2. 📋 Listar vacantes")
        print("3. 👁️  Ver detalle de vacante")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            crear_vacante(db_path)
        elif opcion == "2":
            listar_vacantes(db_path)
        elif opcion == "3":
            ver_detalle_vacante(db_path)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def crear_vacante(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ CREAR NUEVA VACANTE")
    print("=" * 70)
    
    datos = {}
    datos['titulo'] = input("\nTítulo del puesto*: ").strip()
    while not datos['titulo']:
        print("⚠️  El título es obligatorio")
        datos['titulo'] = input("Título del puesto*: ").strip()
    
    datos['departamento'] = input("Departamento: ").strip()
    datos['ubicacion'] = input("Ubicación (Madrid/Avilés/Remoto): ").strip()
    datos['modalidad'] = input("Modalidad (Remoto_Total/Remoto_Parcial/Presencial): ").strip()
    datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    while not datos['stack_obligatorio']:
        print("⚠️  El stack obligatorio es obligatorio")
        datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    
    datos['stack_deseable'] = input("Stack deseable: ").strip()
    
    try:
        datos['rango_salarial_min'] = int(input("Rango salarial mínimo (k€)*: ").strip())
    except ValueError:
        datos['rango_salarial_min'] = 0
    
    try:
        datos['rango_salarial_max'] = int(input("Rango salarial máximo (k€)*: ").strip())
    except ValueError:
        datos['rango_salarial_max'] = 0
    
    datos['responsable'] = input("Responsable de selección*: ").strip()
    while not datos['responsable']:
        print("⚠️  El responsable es obligatorio")
        datos['responsable'] = input("Responsable de selección*: ").strip()
    
    print("\nUrgencia:")
    print("  alta | media | baja")
    datos['urgencia'] = input("Urgencia: ").strip().lower() or 'media'
    
    datos['notas'] = input("\nNotas adicionales: ").strip()
    
    # Generar ID único
    conn = sqlite3.connect(db_path)
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
        datos['titulo'],
        datos.get('departamento'),
        datos.get('ubicacion'),
        datos.get('modalidad'),
        datos['stack_obligatorio'],
        datos.get('stack_deseable'),
        datos['rango_salarial_min'],
        datos['rango_salarial_max'],
        datos['responsable'],
        datos['urgencia'],
        'abierta',
        datetime.now().strftime("%Y-%m-%d"),
        datos.get('notas', '')
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Vacante creada correctamente")
    print(f"   ID: {vacante_id}")
    print(f"   Puesto: {datos['titulo']}")
    pausa()


def listar_vacantes(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 LISTAR VACANTES")
    print("=" * 70)
    
    estado = input("\nFiltrar por estado (abierta/cerrada) - Deja en blanco para todas: ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT id, titulo, departamento, ubicacion, urgencia, estado FROM vacantes"
    params = []
    
    if estado:
        query += " WHERE estado = ?"
        params.append(estado)
    
    query += " ORDER BY fecha_apertura DESC"
    cursor.execute(query, params)
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


def ver_detalle_vacante(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  DETALLE DE VACANTE")
    print("=" * 70)
    
    vid = input("\nID de la vacante: ").strip()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM vacantes WHERE id = ?', (vid,))
    vacante = cursor.fetchone()
    
    if not vacante:
        conn.close()
        print("\n❌ Vacante no encontrada.")
        pausa()
        return
    
    print(f"\n💼 VACANTE: {vacante['titulo']}")
    print(f"{'='*70}")
    print(f"ID:          {vacante['id']}")
    print(f"Departamento:{vacante['departamento'] or '-'}")
    print(f"Ubicación:   {vacante['ubicacion'] or '-'} | Modalidad: {vacante['modalidad'] or '-'}")
    
    print(f"\n🛠️  Requisitos técnicos:")
    print(f"   Obligatorio: {vacante['stack_obligatorio']}")
    print(f"   Deseable:    {vacante['stack_deseable'] or '-'}")
    
    print(f"\n💶 Condiciones:")
    print(f"   Salario: {vacante['rango_salarial_min']}k - {vacante['rango_salarial_max']}k €")
    
    print(f"\n👥 Responsable: {vacante['responsable']}")
    print(f"🚨 Urgencia: {vacante['urgencia'].upper()}")
    print(f"🏷️  Estado: {vacante['estado']}")
    print(f"📅 Apertura: {vacante['fecha_apertura']}")
    
    print(f"\n📝 Notas:")
    print(f"   {vacante['notas'] or '-'}")
    
    print(f"\n⭐ Candidatos finalistas:")
    print(f"   {vacante['candidatos_finalistas'] or 'Ninguno aún'}")
    
    print(f"\n✅ Seleccionado:")
    print(f"   {vacante['candidato_seleccionado'] or 'Pendiente'}")
    
    conn.close()
    pausa()


# ========================================
# MÓDULO 3: PREGUNTAS DE ENTREVISTA
# ========================================

def modulo_preguntas(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   ❓ PREGUNTAS DE ENTREVISTA")
        print("=" * 70)
        print("\n1. 🔍 Buscar preguntas")
        print("2. 📋 Listar todas")
        print("3. ➕ Añadir nueva pregunta")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            buscar_preguntas(db_path)
        elif opcion == "2":
            listar_preguntas(db_path)
        elif opcion == "3":
            anadir_pregunta(db_path)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def buscar_preguntas(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 BUSCAR PREGUNTAS")
    print("=" * 70)
    
    termino = input("\nTérmino de búsqueda (texto o tag): ").strip()
    if not termino:
        print("\n⚠️  Búsqueda vacía.")
        pausa()
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM preguntas 
        WHERE texto LIKE ? OR tags LIKE ?
        ORDER BY categoria, nivel_dificultad DESC
    ''', (f"%{termino}%", f"%{termino}%"))
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print(f"\n📭 No se encontraron preguntas con '{termino}'.")
        pausa()
        return
    
    print(f"\n📊 Encontradas: {len(resultados)} preguntas\n")
    
    categoria_actual = None
    for p in resultados:
        if p[1] != categoria_actual:
            categoria_actual = p[1]
            print(f"\n{'='*70}")
            print(f"📌 CATEGORÍA: {categoria_actual.upper()}")
            print('='*70)
        
        sub = f" | {p[2]}" if p[2] else ""
        print(f"\n[ID: {p[0]}] ({p[4][:1].upper()}){sub}")
        print(f"❓ {p[3]}")
        if p[5]:
            print(f"🏷️  Tags: {p[5]}")
    
    pausa()


def listar_preguntas(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 TODAS LAS PREGUNTAS")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
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
        print(f"\n[ID: {p[0]}] ({p[4][:1].upper()}){sub}")
        print(f"❓ {p[3]}")
        if p[5]:
            print(f"🏷️  Tags: {p[5]}")
    
    pausa()


def anadir_pregunta(db_path):
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
        subcategoria = input("Subcategoría (ej: backend, devops): ").strip().lower()
    
    texto = input("\nPregunta*: ").strip()
    while not texto:
        print("⚠️  La pregunta no puede estar vacía")
        texto = input("Pregunta*: ").strip()
    
    print("\nNivel dificultad: facil | medio | dificil")
    nivel = input("Nivel dificultad [medio]: ").strip().lower() or 'medio'
    
    tags = input("Tags (separados por comas): ").strip()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO preguntas (categoria, subcategoria, texto, nivel_dificultad, tags)
        VALUES (?, ?, ?, ?, ?)
    ''', (categoria, subcategoria, texto, nivel, tags))
    conn.commit()
    conn.close()
    
    print("\n✅ Pregunta añadida correctamente.")
    pausa()


# ========================================
# MÓDULO 4: PERFILES SELECCIONADOS POR LA EMPRESA
# ========================================

def modulo_perfiles_empresa(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   👥 PERFILES SELECCIONADOS POR LA EMPRESA")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
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
    
    print(f"\n{'─'*70}")
    pausa()


# ========================================
# MÓDULO 5: PRESENTACIÓN DE EMPRESA
# ========================================

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


# ========================================
# MÓDULO 6: METODOLOGÍAS ÁGILES
# ========================================

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


# ========================================
# MÓDULO 7: CONVENIO OFICINAS MADRID
# ========================================

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


# ========================================
# MÓDULO 8: ESTATUTO DE LOS TRABAJADORES
# ========================================

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


# ========================================
# MÓDULO 9: ASOCIACIONES COLABORACIÓN
# ========================================

def modulo_asociaciones(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   ♿ ASOCIACIONES CON LAS QUE COLABORAR")
        print("=" * 70)
        print("\n1. 👁️  Ver asociaciones por tipo")
        print("2. ➕ Añadir nueva asociación")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            ver_asociaciones(db_path)
        elif opcion == "2":
            anadir_asociacion(db_path)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def ver_asociaciones(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   ♿ ASOCIACIONES POR TIPO")
    print("=" * 70)
    
    print("\nTipos disponibles: discapacidad | mujeres | otras")
    tipo = input("\nFiltrar por tipo (deja en blanco para todas): ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
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


def anadir_asociacion(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ AÑADIR NUEVA ASOCIACIÓN")
    print("=" * 70)
    
    nombre = input("\nNombre*: ").strip()
    while not nombre:
        print("⚠️  El nombre es obligatorio")
        nombre = input("Nombre*: ").strip()
    
    print("\nTipos: discapacidad | mujeres | otras")
    tipo = input("Tipo*: ").strip().lower()
    while tipo not in ['discapacidad', 'mujeres', 'otras']:
        print("⚠️  Tipo no válido")
        tipo = input("Tipo*: ").strip().lower()
    
    contacto = input("Contacto: ").strip()
    web = input("Web: ").strip()
    notas = input("Notas: ").strip()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO asociaciones (nombre, tipo, contacto, web, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, tipo, contacto, web, notas))
    conn.commit()
    conn.close()
    
    print("\n✅ Asociación añadida correctamente.")
    pausa()


# ========================================
# MÓDULO 10: CENTROS DE PRÁCTICAS
# ========================================

def modulo_centros_practicas(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🎓 CENTROS DE PRÁCTICAS")
    print("=" * 70)
    print("""
Centros colaboradores para prácticas formativas:

UNIVERSIDADES
• Universidad Politécnica de Madrid (UPM)
  - Grados: Ingeniería Informática, Telecomunicaciones
  - Contacto: practicas@upm.es
  
• Universidad Carlos III de Madrid (UC3M)
  - Grados: Ingeniería de Software, Sistemas de Telecomunicación
  - Contacto: empresas.leganes@uc3m.es
  
• Universidad de Oviedo
  - Campus: Gijón (proximidad a oficinas Avilés)
  - Grados: Ingeniería Informática, Telecomunicaciones
  - Contacto: practicas@uniovi.es

FP SUPERIOR
• IES Virgen de la Paloma (Madrid)
  - Ciclos: DAM, DAW, Administración de Sistemas
  - Contacto: secretaria@iesvirgendelapaloma.es
  
• IES La Magdalena (Avilés)
  - Ciclos: DAM, Redes y Sistemas
  - Contacto: ieslamagdalena@eduastur.es

PROCEDIMIENTO PRÁCTICAS
1. Contactar con departamento de prácticas del centro
2. Firmar convenio específico (modelo empresa)
3. Asignar tutor interno empresa
4. Definir plan de actividades y objetivos
5. Seguimiento quincenal y evaluación final

⚠️  Requisitos legales:
• Seguro escolar obligatorio
• Duración máxima: 9 meses (FP) / 6 meses (universidad)
• Horario: máximo 6 horas/día, 30 horas/semana
• No sustitución de personal contratado
""")
    print("=" * 70)
    pausa()


# ========================================
# MÓDULO 11: PORTALES DE EMPLEO
# ========================================

def modulo_portales_empleo(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   💼 PORTALES DE EMPLEO")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
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


# ========================================
# MÓDULO 12: PLANTILLAS VACANTES
# ========================================

def modulo_plantillas_vacantes(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   📄 PLANTILLAS DE VACANTES PARA PUBLICAR")
    print("=" * 70)
    print("""
Plantillas predefinidas para publicación rápida:

BACKEND DEVELOPER (Java/Spring)
───────────────────────────────────────────────────────────────────────
¿Quieres desarrollar software crítico para operadores de telecom?
Buscamos Backend Developer para unirse a nuestro equipo de producto OSS.

Stack: Java 17, Spring Boot 3, PostgreSQL, Kubernetes, AWS/Azure
Metodología: Scrum + DevOps (GitLab CI/CD)
Modalidad: 100% remoto o híbrido (Madrid/Avilés)

Requisitos:
• 3+ años experiencia Java/Spring en entornos cloud
• Experiencia con microservicios y APIs REST
• Conocimientos de SQL y bases de datos relacionales
• Inglés técnico (B2 mínimo)

Ofrecemos:
• Salario: 38.000€ - 52.000€ (según experiencia)
• Proyectos estables de largo plazo con clientes internacionales
• Formación continua en estándares TM Forum y ODA
• Equipo técnico senior y ambiente colaborativo

───────────────────────────────────────────────────────────────────────

DEVOPS ENGINEER
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


# ========================================
# MÓDULO 13: TEAM BUILDING
# ========================================

def modulo_team_building(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🤝 TEAM BUILDING POR CATEGORÍAS")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT categoria FROM team_building ORDER BY categoria')
    categorias = cursor.fetchall()
    
    print("\nCategorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        cursor.execute('SELECT COUNT(*) FROM team_building WHERE categoria = ?', (cat[0],))
        count = cursor.fetchone()[0]
        print(f"  {i}. {cat[0].capitalize()} ({count} actividades)")
    
    print("\n0. Ver todas las actividades")
    opcion = input("\n➤ Selecciona categoría (número) o 0 para todas: ").strip()
    
    if opcion == "0":
        cursor.execute('SELECT * FROM team_building ORDER BY categoria, nombre_actividad')
        actividades = cursor.fetchall()
    else:
        try:
            idx = int(opcion) - 1
            categoria_sel = categorias[idx][0]
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


# ========================================
# MÓDULO 14: GLOSARIO
# ========================================

def modulo_glosario(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   📖 GLOSARIO DE TÉRMINOS")
    print("=" * 70)
    
    print("\nCategorías disponibles: técnico | metodologia | legal | telecom | rrhh | todas")
    categoria = input("\nFiltrar por categoría (deja en blanco para todas): ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if categoria and categoria != 'todas':
        cursor.execute('SELECT * FROM glosario WHERE categoria = ? ORDER BY termino', (categoria,))
    else:
        cursor.execute('SELECT * FROM glosario ORDER BY categoria, termino')
    
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No hay términos con esos criterios.")
        pausa()
        return
    
    categoria_actual = None
    for g in resultados:
        if g[3] != categoria_actual:
            categoria_actual = g[3]
            print(f"\n{'='*70}")
            print(f"📌 CATEGORÍA: {categoria_actual.upper()}")
            print('='*70)
        
        print(f"\n🔹 {g[1]}")
        print(f"   {g[2]}")
    
    pausa()


# ========================================
# MENÚ PRINCIPAL
# ========================================

def menu_principal(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📋 APLICACIÓN INTEGRAL DE SELECCIÓN Y RECLUTAMIENTO")
        print("=" * 70)
        print("\n1. 👥 Base de datos de candidatos")
        print("2. 💼 Selección de la empresa (vacantes)")
        print("3. ❓ Preguntas de entrevista")
        print("4. 👤 Perfiles seleccionados por la empresa")
        print("5. 🏢 Presentación de empresa")
        print("6. 🚀 Metodologías ágiles")
        print("7. 📋 Convenio oficinas Madrid")
        print("8. 📜 Estatuto de los trabajadores")
        print("9. ♿ Asociaciones colaboración")
        print("10. 🎓 Centros de prácticas")
        print("11. 💼 Portales de empleo")
        print("12. 📄 Plantillas vacantes")
        print("13. 🤝 Team building")
        print("14. 📖 Glosario de términos")
        print("0. ❌ Salir")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-14): ").strip()
        
        if opcion == "1":
            modulo_candidatos(db_path)
        elif opcion == "2":
            modulo_vacantes(db_path)
        elif opcion == "3":
            modulo_preguntas(db_path)
        elif opcion == "4":
            modulo_perfiles_empresa(db_path)
        elif opcion == "5":
            modulo_presentacion_empresa()
        elif opcion == "6":
            modulo_metodologias_agiles()
        elif opcion == "7":
            modulo_convenio_madrid()
        elif opcion == "8":
            modulo_estatuto_trabajadores()
        elif opcion == "9":
            modulo_asociaciones(db_path)
        elif opcion == "10":
            modulo_centros_practicas(db_path)
        elif opcion == "11":
            modulo_portales_empleo(db_path)
        elif opcion == "12":
            modulo_plantillas_vacantes(db_path)
        elif opcion == "13":
            modulo_team_building(db_path)
        elif opcion == "14":
            modulo_glosario(db_path)
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto!")
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    # Crear carpeta data si no existe
    if not os.path.exists("data"):
        print("📁 Creando carpeta 'data' para la base de datos...")
        os.makedirs("data", exist_ok=True)
    
    # Inicializar base de datos
    db_path = inicializar_db()
    print("✅ Base de datos inicializada correctamente")
    pausa()
    
    # Ejecutar menú principal
    try:
        menu_principal(db_path)
    except KeyboardInterrupt:
        print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        pausa()
