#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
App RRHH Alvatross - Módulos: candidatos, vacantes, evaluaciones R/S/T
Stack: TM Forum, ODA, OSS/BSS, Java/Spring, Kubernetes
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import os
import sys


# ========================================
# CONFIGURACIÓN GLOBAL
# ========================================

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


# ========================================
# BASE DE DATOS - INICIALIZACIÓN
# ========================================

def inicializar_db():
    """Crear base de datos y tablas si no existen"""
    db_path = Path("data") / "rrhh_alvatross.db"
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
            carnet_conducir BOOLEAN DEFAULT 0,
            vehiculo_propio BOOLEAN DEFAULT 0,
            nivel_estudios TEXT,
            titulacion TEXT,
            certificaciones TEXT,
            idiomas TEXT,
            experiencia_total INTEGER DEFAULT 0,
            experiencia_telecom INTEGER DEFAULT 0,
            experiencia_tmforum TEXT,
            ultimo_puesto TEXT,
            ultima_empresa TEXT,
            proyectos TEXT,
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
            perfil_it TEXT NOT NULL,
            seniority TEXT NOT NULL,
            departamento TEXT,
            ubicacion TEXT,
            modalidad TEXT,
            stack_obligatorio TEXT NOT NULL,
            stack_deseable TEXT,
            experiencia_tmforum TEXT,
            experiencia_telecom TEXT,
            certificaciones_requeridas TEXT,
            rango_salarial_min INTEGER,
            rango_salarial_max INTEGER,
            tipo_contrato TEXT,
            jornada TEXT,
            necesidad TEXT,
            responsable_seleccion TEXT,
            responsable_tecnico TEXT,
            hiring_manager TEXT,
            fecha_apertura TEXT NOT NULL,
            fecha_cierre_estimada TEXT,
            fecha_cierre_real TEXT,
            estado TEXT DEFAULT 'abierta',
            time_to_hire INTEGER,
            candidatos_totales INTEGER DEFAULT 0,
            candidatos_finalistas INTEGER DEFAULT 0,
            candidato_seleccionado TEXT,
            notas TEXT
        )
    ''')
    
    # Tabla evaluaciones R/S/T
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
            tipo_entrevista TEXT,
            FOREIGN KEY (candidato_id) REFERENCES candidatos(id),
            FOREIGN KEY (vacante_id) REFERENCES vacantes(id)
        )
    ''')
    
    # Tabla interacciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id TEXT NOT NULL,
            fecha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            responsable TEXT,
            notas TEXT,
            proximo_paso TEXT,
            FOREIGN KEY (candidato_id) REFERENCES candidatos(id)
        )
    ''')
    
    # Tabla asociación candidato-vacante
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidato_vacante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id TEXT NOT NULL,
            vacante_id TEXT NOT NULL,
            fase TEXT DEFAULT 'screening',
            fecha_asignacion TEXT NOT NULL,
            notas_fase TEXT,
            FOREIGN KEY (candidato_id) REFERENCES candidatos(id),
            FOREIGN KEY (vacante_id) REFERENCES vacantes(id),
            UNIQUE(candidato_id, vacante_id)
        )
    ''')
    
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
# CRUD CANDIDATOS
# ========================================

def crear_candidato(db_path):
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
    datos['github'] = input("GitHub/GitLab URL: ").strip()
    datos['localizacion'] = input("Ciudad/Provincia: ").strip()
    datos['remoto'] = input("Disponibilidad remoto (Total/Parcial/Presencial): ").strip()
    datos['disponibilidad'] = input("Disponibilidad incorporación (Inmediata/15d/30d/60d+): ").strip()
    datos['carnet_conducir'] = 1 if input("¿Carnet de conducir? (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', '') else 0
    datos['vehiculo_propio'] = 1 if input("¿Vehículo propio? (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', '') else 0
    datos['nivel_estudios'] = input("Nivel de estudios (Grado/Máster/FP/Doctorado): ").strip()
    datos['titulacion'] = input("Titulación específica: ").strip()
    datos['certificaciones'] = input("Certificaciones relevantes: ").strip()
    datos['idiomas'] = input("Idiomas (ej: Inglés C1, Francés B2): ").strip()
    
    try:
        datos['experiencia_total'] = int(input("Años totales en IT: ").strip() or "0")
    except ValueError:
        datos['experiencia_total'] = 0
    
    try:
        datos['experiencia_telecom'] = int(input("Años en telecom/OSS/BSS: ").strip() or "0")
    except ValueError:
        datos['experiencia_telecom'] = 0
    
    datos['ultimo_puesto'] = input("Último puesto: ").strip()
    datos['ultima_empresa'] = input("Última empresa: ").strip()
    datos['proyectos'] = input("Proyectos relevantes: ").strip()
    datos['experiencia_tmforum'] = input("Experiencia TM Forum/ODA (Sí/No/Nivel): ").strip()
    datos['stack_lenguajes'] = input("Lenguajes (ej: Java, Python, TypeScript): ").strip()
    datos['stack_frameworks'] = input("Frameworks (ej: Spring Boot, Angular, React): ").strip()
    datos['stack_bbdd'] = input("Bases de datos (ej: Oracle, PostgreSQL): ").strip()
    datos['stack_cloud'] = input("Cloud (AWS/Azure/GCP): ").strip()
    datos['stack_devops'] = input("DevOps (Docker, Kubernetes, Terraform): ").strip()
    datos['stack_apis'] = input("APIs/Integración (REST, TMForum, SOAP): ").strip()
    datos['stack_mensajeria'] = input("Mensajería (Kafka, RabbitMQ): ").strip()
    datos['competencias'] = input("Competencias blandas: ").strip()
    datos['salario_esperado'] = input("Expectativa salarial (k€): ").strip()
    
    print("\nPerfiles IT:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    datos['perfil_it'] = input("\nPerfil IT*: ").strip().lower()
    while datos['perfil_it'] not in PERFILES_IT:
        print("⚠️  Perfil no válido")
        datos['perfil_it'] = input("Perfil IT*: ").strip().lower()
    
    print("\nSeniority:")
    for key, value in SENIORITY_NIVELES.items():
        print(f"  {key:10} - {value}")
    datos['seniority'] = input("\nSeniority*: ").strip().lower()
    while datos['seniority'] not in SENIORITY_NIVELES:
        print("⚠️  Seniority no válido")
        datos['seniority'] = input("Seniority*: ").strip().lower()
    
    datos['notas'] = input("\nNotas iniciales: ").strip()
    gdpr = input("\n✅ ¿Consentimiento GDPR registrado? (S/n): ").strip().lower()
    datos['gdpr_consent'] = 1 if gdpr in ('', 's', 'si', 'yes') else 0
    
    # Guardar en BD
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    cursor.execute('''
        INSERT INTO candidatos (
            id, nombre, email, telefono, linkedin, github, localizacion,
            remoto, disponibilidad, carnet_conducir, vehiculo_propio,
            nivel_estudios, titulacion, certificaciones, idiomas,
            experiencia_total, experiencia_telecom, experiencia_tmforum,
            ultimo_puesto, ultima_empresa, proyectos,
            stack_lenguajes, stack_frameworks, stack_bbdd, stack_cloud,
            stack_devops, stack_apis, stack_mensajeria,
            competencias, salario_esperado, estado, perfil_it, seniority,
            gdpr_consent, fecha_registro, origen, notas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        datos['carnet_conducir'],
        datos['vehiculo_propio'],
        datos.get('nivel_estudios'),
        datos.get('titulacion'),
        datos.get('certificaciones'),
        datos.get('idiomas'),
        datos['experiencia_total'],
        datos['experiencia_telecom'],
        datos.get('experiencia_tmforum'),
        datos.get('ultimo_puesto'),
        datos.get('ultima_empresa'),
        datos.get('proyectos'),
        datos.get('stack_lenguajes'),
        datos.get('stack_frameworks'),
        datos.get('stack_bbdd'),
        datos.get('stack_cloud'),
        datos.get('stack_devops'),
        datos.get('stack_apis'),
        datos.get('stack_mensajeria'),
        datos.get('competencias'),
        datos.get('salario_esperado'),
        'activo',
        datos['perfil_it'],
        datos['seniority'],
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
    print(f"   Perfil: {PERFILES_IT[datos['perfil_it']]}")
    pausa()


def listar_candidatos(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 LISTAR CANDIDATOS")
    print("=" * 70)
    
    buscar = input("\nBuscar (nombre, stack, puesto) - Deja en blanco para todos: ").strip()
    estado = input("Filtrar por estado (activo/screening/entrevista/offer) - Deja en blanco: ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT id, nombre, email, telefono, ultimo_puesto, stack_lenguajes, perfil_it, seniority, estado FROM candidatos WHERE estado != 'archivado'"
    params = []
    
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    
    if buscar:
        query += " AND (nombre LIKE ? OR stack_lenguajes LIKE ? OR ultimo_puesto LIKE ?)"
        buscar_param = f"%{buscar}%"
        params.extend([buscar_param, buscar_param, buscar_param])
    
    query += " ORDER BY fecha_registro DESC"
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        print("\n📭 No se encontraron candidatos.")
        pausa()
        return
    
    print(f"\n📊 Encontrados: {len(resultados)} candidatos\n")
    print(f"{'ID':<15} {'Nombre':<25} {'Puesto':<20} {'Perfil':<15} {'Seniority':<10} {'Estado':<12}")
    print("-" * 95)
    
    for row in resultados:
        perfil = row[6][:15] if row[6] else '-'
        print(f"{row[0]:<15} {row[1][:23]:<25} {row[4][:18] if row[4] else '-':<20} "
              f"{perfil:<15} {row[7] or '-':<10} {row[8]:<12}")
    
    pausa()


# ========================================
# CRUD VACANTES
# ========================================

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
    
    print("\nPerfiles IT:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    datos['perfil_it'] = input("\nPerfil IT*: ").strip().lower()
    while datos['perfil_it'] not in PERFILES_IT:
        print("⚠️  Perfil no válido")
        datos['perfil_it'] = input("Perfil IT*: ").strip().lower()
    
    print("\nSeniority:")
    for key, value in SENIORITY_NIVELES.items():
        print(f"  {key:10} - {value}")
    datos['seniority'] = input("\nSeniority*: ").strip().lower()
    while datos['seniority'] not in SENIORITY_NIVELES:
        print("⚠️  Seniority no válido")
        datos['seniority'] = input("Seniority*: ").strip().lower()
    
    datos['departamento'] = input("Departamento (Desarrollo/DevOps/Producto/Arquitectura/Operaciones): ").strip()
    datos['ubicacion'] = input("Ubicación (Madrid/Avilés/Remoto): ").strip()
    datos['modalidad'] = input("Modalidad (Remoto_Total/Remoto_Parcial/Presencial): ").strip()
    datos['stack_obligatorio'] = input("\nStack obligatorio*: ").strip()
    while not datos['stack_obligatorio']:
        print("⚠️  El stack obligatorio es obligatorio")
        datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    
    datos['stack_deseable'] = input("Stack deseable: ").strip()
    datos['experiencia_tmforum'] = input("Experiencia TM Forum/ODA (Obligatorio/Deseable/No_relevante): ").strip()
    datos['experiencia_telecom'] = input("Experiencia Telecom OSS/BSS (Obligatorio/Deseable/No_relevante): ").strip()
    datos['certificaciones_requeridas'] = input("Certificaciones requeridas: ").strip()
    
    try:
        datos['rango_salarial_min'] = int(input("\nRango salarial mínimo (k€)*: ").strip())
    except ValueError:
        datos['rango_salarial_min'] = 0
    
    try:
        datos['rango_salarial_max'] = int(input("Rango salarial máximo (k€)*: ").strip())
    except ValueError:
        datos['rango_salarial_max'] = 0
    
    datos['tipo_contrato'] = input("Tipo de contrato (Indefinido/Temporal): ").strip()
    datos['jornada'] = input("Jornada (Completa/Parcial): ").strip()
    datos['necesidad'] = input("Tipo de necesidad (Nueva/Reemplazo): ").strip()
    datos['responsable_seleccion'] = input("\nResponsable de selección (RRHH)*: ").strip()
    while not datos['responsable_seleccion']:
        print("⚠️  El responsable es obligatorio")
        datos['responsable_seleccion'] = input("Responsable de selección (RRHH)*: ").strip()
    
    datos['responsable_tecnico'] = input("Responsable técnico (Tech Lead/Arquitecto): ").strip()
    datos['hiring_manager'] = input("Hiring Manager (Jefe de Área): ").strip()
    datos['fecha_cierre_estimada'] = input("\nFecha cierre estimada (YYYY-MM-DD, opcional): ").strip()
    datos['notas'] = input("Notas adicionales: ").strip()
    
    # Generar ID único
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM vacantes WHERE id LIKE ?', (f"ALV-{datetime.now().year}%",))
    count = cursor.fetchone()[0] + 1
    vacante_id = f"ALV-{datetime.now().year}-{count:03d}"
    
    cursor.execute('''
        INSERT INTO vacantes (
            id, titulo, perfil_it, seniority, departamento, ubicacion, modalidad,
            stack_obligatorio, stack_deseable, experiencia_tmforum, experiencia_telecom,
            certificaciones_requeridas, rango_salarial_min, rango_salarial_max,
            tipo_contrato, jornada, necesidad, responsable_seleccion,
            responsable_tecnico, hiring_manager, fecha_apertura,
            fecha_cierre_estimada, estado, notas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        vacante_id,
        datos['titulo'],
        datos['perfil_it'],
        datos['seniority'],
        datos.get('departamento'),
        datos.get('ubicacion'),
        datos.get('modalidad'),
        datos['stack_obligatorio'],
        datos.get('stack_deseable'),
        datos.get('experiencia_tmforum'),
        datos.get('experiencia_telecom'),
        datos.get('certificaciones_requeridas'),
        datos['rango_salarial_min'],
        datos['rango_salarial_max'],
        datos.get('tipo_contrato'),
        datos.get('jornada'),
        datos.get('necesidad'),
        datos['responsable_seleccion'],
        datos.get('responsable_tecnico'),
        datos.get('hiring_manager'),
        datetime.now().strftime("%Y-%m-%d"),
        datos.get('fecha_cierre_estimada'),
        'abierta',
        datos.get('notas', '')
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Vacante creada correctamente")
    print(f"   ID: {vacante_id}")
    print(f"   Puesto: {datos['titulo']}")
    print(f"   Perfil: {PERFILES_IT[datos['perfil_it']]} ({datos['seniority'].upper()})")
    pausa()


def listar_vacantes(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 LISTAR VACANTES")
    print("=" * 70)
    
    estado = input("\nFiltrar por estado (abierta/cerrada_cubierta) - Deja en blanco para todas: ").strip().lower() or None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT id, titulo, perfil_it, seniority, ubicacion, estado FROM vacantes"
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
    print(f"{'ID':<15} {'Título':<30} {'Perfil':<20} {'Ubicación':<15} {'Estado':<15}")
    print("-" * 95)
    
    for row in resultados:
        perfil = PERFILES_IT.get(row[2], row[2])[:20]
        print(f"{row[0]:<15} {row[1][:28]:<30} {perfil:<20} {row[4] or '-':<15} {row[5]:<15}")
    
    pausa()


# ========================================
# EVALUACIONES R/S/T
# ========================================

def crear_evaluacion(db_path):
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ NUEVA EVALUACIÓN R/S/T")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, perfil_it FROM candidatos WHERE id = ?', (cid,))
    candidato = cursor.fetchone()
    
    if not candidato:
        conn.close()
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato[0]}")
    print(f"Perfil: {PERFILES_IT.get(candidato[1], candidato[1])}")
    
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
    print("   1-3: respuestas vagas, sin ejemplos")
    print("   4-6: base correcta, algunos ejemplos")
    print("   7-8: sólido, ejemplos claros")
    print("   9-10: excelente, liderazgo/ownership")
    try:
        r_puntuacion = int(input("Puntuación R (1-10)*: ").strip())
    except ValueError:
        r_puntuacion = 0
    r_notas = input("Notas R: ").strip()
    
    print("\n--- Dimensión S: Técnica/Stack (1-10) ---")
    try:
        s_puntuacion = int(input("Puntuación S (1-10)*: ").strip())
    except ValueError:
        s_puntuacion = 0
    s_notas = input("Notas S: ").strip()
    
    print("\n--- Dimensión T: Cultural/Soft Skills (1-10) ---")
    print("   Alineación DevSecOps, colaboración, estabilidad")
    try:
        t_puntuacion = int(input("Puntuación T (1-10)*: ").strip())
    except ValueError:
        t_puntuacion = 0
    t_notas = input("Notas T: ").strip()
    
    # Calcular score final con ponderación por perfil
    perfil = candidato[1] or 'backend'
    ponderacion = {
        'backend': (0.20, 0.60, 0.20),
        'devops': (0.20, 0.60, 0.20),
        'qa': (0.25, 0.50, 0.25),
        'solution_architect': (0.25, 0.50, 0.25),
        'product_owner': (0.30, 0.40, 0.30),
        'integrations': (0.20, 0.60, 0.20),
        'support': (0.30, 0.40, 0.30),
        'frontend': (0.25, 0.50, 0.25)
    }
    p_r, p_s, p_t = ponderacion.get(perfil, (0.25, 0.50, 0.25))
    score_final = round((r_puntuacion * p_r) + (s_puntuacion * p_s) + (t_puntuacion * p_t), 2)
    
    print(f"\n➤ Score final calculado: {score_final}/10")
    
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
            score_final, recomendacion, tipo_entrevista
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        cid,
        vid if vid else None,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        evaluador,
        r_puntuacion, r_notas,
        s_puntuacion, s_notas,
        t_puntuacion, t_notas,
        score_final,
        recomendacion,
        'general'
    ))
    
    # Actualizar estado si score alto
    if score_final >= 7.0:
        cursor.execute('UPDATE candidatos SET estado = ? WHERE id = ?', ('entrevista', cid))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Evaluación registrada correctamente")
    print(f"   Score final: {score_final}/10")
    print(f"   Recomendación: {recomendacion}")
    pausa()


# ========================================
# MENÚ PRINCIPAL
# ========================================

def menu_principal(db_path):
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📋 APP RRHH ALVATROSS - Grupo SATEC")
        print("=" * 70)
        print("\n1. 👥 Gestión de Candidatos")
        print("2. 💼 Gestión de Vacantes")
        print("3. 📊 Evaluaciones R/S/T")
        print("0. ❌ Salir")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-3): ").strip()
        
        if opcion == "1":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   👥 GESTIÓN DE CANDIDATOS")
                print("=" * 70)
                print("\n1. 🆕 Registrar nuevo candidato")
                print("2. 🔍 Listar candidatos")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_candidato(db_path)
                elif subopcion == "2":
                    listar_candidatos(db_path)
                elif subopcion == "0":
                    break
        
        elif opcion == "2":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   💼 GESTIÓN DE VACANTES")
                print("=" * 70)
                print("\n1. ➕ Crear nueva vacante")
                print("2. 📋 Listar vacantes")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_vacante(db_path)
                elif subopcion == "2":
                    listar_vacantes(db_path)
                elif subopcion == "0":
                    break
        
        elif opcion == "3":
            while True:
                limpiar_pantalla()
                print("=" * 70)
                print("   📊 EVALUACIONES R/S/T")
                print("=" * 70)
                print("\n1. ➕ Nueva evaluación")
                print("0. ⬅️  Volver")
                print("-" * 70)
                
                subopcion = input("\n➤ Opción: ").strip()
                if subopcion == "1":
                    crear_evaluacion(db_path)
                elif subopcion == "0":
                    break
        
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto! Que el stack te acompañe.")
            break
        
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    # Inicializar base de datos
    db_path = inicializar_db()
    
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
