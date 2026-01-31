#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Menú principal de la app RRHH Alvatross - Grupo SATEC
Módulos completos: candidatos, vacantes, evaluaciones R/S/T, asociaciones
"""

from database import DatabaseManager
from datetime import datetime
import os
import sys


# ========================================
# CONFIGURACIÓN Y UTILIDADES
# ========================================

def limpiar_pantalla():
    """Limpia la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    """Pausa hasta que el usuario pulse Enter"""
    input("\n↲ Pulsa Enter para continuar...")


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
# MENÚ PRINCIPAL
# ========================================

def menu_principal():
    """Menú principal de la aplicación"""
    db = DatabaseManager()
    
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📋 APP RRHH ALVATROSS - Grupo SATEC")
        print("=" * 70)
        print("\n1. 👥 Gestión de Candidatos")
        print("2. 💼 Gestión de Vacantes")
        print("3. 📊 Evaluaciones R/S/T")
        print("4. 🔄 Asociar Candidato-Vacante")
        print("5. 📤 Exportar Datos")
        print("0. ❌ Salir")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-5): ").strip()
        
        if opcion == "1":
            menu_candidatos(db)
        elif opcion == "2":
            menu_vacantes(db)
        elif opcion == "3":
            menu_evaluaciones(db)
        elif opcion == "4":
            menu_asociaciones(db)
        elif opcion == "5":
            menu_exportacion(db)
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto! Que el stack te acompañe.")
            db.disconnect()
            break
        else:
            print("\n⚠️  Opción no válida. Inténtalo de nuevo.")
            pausa()


# ========================================
# MENÚ CANDIDATOS
# ========================================

def menu_candidatos(db):
    """Menú de gestión de candidatos"""
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   👥 GESTIÓN DE CANDIDATOS")
        print("=" * 70)
        print("\n1. 🆕 Registrar nuevo candidato")
        print("2. 🔍 Buscar/Listar candidatos")
        print("3. 👁️  Ver detalle de candidato")
        print("4. ✏️  Editar candidato")
        print("5. 📞 Registrar interacción")
        print("6. 🗑️  Archivar candidato")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-6): ").strip()
        
        if opcion == "1":
            registrar_candidato(db)
        elif opcion == "2":
            listar_candidatos(db)
        elif opcion == "3":
            ver_detalle_candidato(db)
        elif opcion == "4":
            editar_candidato(db)
        elif opcion == "5":
            registrar_interaccion(db)
        elif opcion == "6":
            archivar_candidato(db)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def registrar_candidato(db):
    """Formulario para registrar un nuevo candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   🆕 REGISTRAR NUEVO CANDIDATO")
    print("=" * 70)
    print("(Campos obligatorios marcados con *)\n")
    
    datos = {}
    
    # Datos obligatorios
    while not datos.get('nombre'):
        datos['nombre'] = input("Nombre completo*: ").strip()
        if not datos['nombre']:
            print("⚠️  El nombre es obligatorio")
    
    datos['email'] = input("Email: ").strip()
    datos['telefono'] = input("Teléfono: ").strip()
    datos['linkedin'] = input("LinkedIn URL: ").strip()
    datos['github'] = input("GitHub/GitLab URL: ").strip()
    
    print("\n--- Localización y disponibilidad ---")
    datos['localizacion'] = input("Ciudad/Provincia: ").strip()
    datos['remoto'] = input("Disponibilidad remoto (Total/Parcial/Presencial): ").strip()
    datos['disponibilidad'] = input("Disponibilidad incorporación (Inmediata/15d/30d/60d+): ").strip()
    datos['carnet_conducir'] = 1 if input("¿Carnet de conducir? (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', '') else 0
    datos['vehiculo_propio'] = 1 if input("¿Vehículo propio? (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', '') else 0
    
    print("\n--- Formación ---")
    datos['nivel_estudios'] = input("Nivel de estudios (Grado/Máster/FP/Doctorado): ").strip()
    datos['titulacion'] = input("Titulación específica: ").strip()
    datos['certificaciones'] = input("Certificaciones relevantes (separadas por comas): ").strip()
    datos['idiomas'] = input("Idiomas (ej: Inglés C1, Francés B2): ").strip()
    
    print("\n--- Experiencia ---")
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
    datos['proyectos'] = input("Proyectos relevantes (breve): ").strip()
    datos['experiencia_tmforum'] = input("Experiencia TM Forum/ODA (Sí/No/Nivel): ").strip()
    
    print("\n--- Stack técnico ---")
    datos['stack_lenguajes'] = input("Lenguajes (ej: Java, Python, TypeScript): ").strip()
    datos['stack_frameworks'] = input("Frameworks (ej: Spring Boot, Angular, React): ").strip()
    datos['stack_bbdd'] = input("Bases de datos (ej: Oracle, PostgreSQL, MongoDB): ").strip()
    datos['stack_cloud'] = input("Cloud (AWS/Azure/GCP): ").strip()
    datos['stack_devops'] = input("DevOps (Docker, Kubernetes, Terraform...): ").strip()
    datos['stack_apis'] = input("APIs/Integración (REST, TMForum, SOAP...): ").strip()
    datos['stack_mensajeria'] = input("Mensajería (Kafka, RabbitMQ...): ").strip()
    
    print("\n--- Competencias blandas ---")
    datos['competencias'] = input("Competencias (ej: Comunicación, Ownership, Trabajo en equipo): ").strip()
    
    print("\n--- RRHH y preferencias ---")
    datos['salario_esperado'] = input("Expectativa salarial (k€): ").strip()
    
    # Perfil IT
    print("\nPerfiles IT disponibles:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    datos['perfil_it'] = input("\nPerfil IT (ej: backend, devops): ").strip().lower()
    
    # Seniority
    print("\nNiveles de seniority:")
    for key, value in SENIORITY_NIVELES.items():
        print(f"  {key:10} - {value}")
    datos['seniority'] = input("\nSeniority (junior/mid/senior/lead): ").strip().lower()
    
    datos['notas'] = input("\nNotas iniciales: ").strip()
    
    # GDPR
    gdpr = input("\n✅ ¿Consentimiento GDPR registrado? (S/n): ").strip().lower()
    datos['gdpr_consent'] = 1 if gdpr in ('', 's', 'si', 'yes') else 0
    
    # Guardar en BD
    candidato_id = db.crear_candidato(datos)
    
    print(f"\n✅ Candidato registrado correctamente")
    print(f"   ID: {candidato_id}")
    print(f"   Nombre: {datos['nombre']}")
    print(f"   Perfil: {PERFILES_IT.get(datos['perfil_it'], datos['perfil_it'])}")
    print(f"   Seniority: {SENIORITY_NIVELES.get(datos['seniority'], datos['seniority'])}")
    
    pausa()


def listar_candidatos(db):
    """Listar candidatos con búsqueda y filtros"""
    limpiar_pantalla()
    print("=" * 70)
    print("   🔍 LISTAR CANDIDATOS")
    print("=" * 70)
    
    buscar = input("\nBuscar (nombre, stack, puesto) - Deja en blanco para mostrar todos: ").strip()
    estado = input("Filtrar por estado (activo/screening/entrevista/offer/descartado) - Deja en blanco para todos: ").strip().lower() or None
    
    print("\nPerfiles IT disponibles para filtrar:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    perfil_filtro = input("\nFiltrar por perfil IT (deja en blanco para todos): ").strip().lower() or None
    
    candidatos = db.listar_candidatos(filtro_estado=estado, buscar=buscar, perfil_it=perfil_filtro)
    
    if not candidatos:
        print("\n📭 No se encontraron candidatos con esos criterios.")
        pausa()
        return
    
    print(f"\n📊 Encontrados: {len(candidatos)} candidatos\n")
    print(f"{'ID':<15} {'Nombre':<25} {'Puesto':<20} {'Perfil':<15} {'Seniority':<10} {'Estado':<12}")
    print("-" * 95)
    
    for c in candidatos:
        perfil = c['perfil_it'][:15] if c['perfil_it'] else '-'
        print(f"{c['id']:<15} {c['nombre'][:23]:<25} {c['ultimo_puesto'][:18] if c['ultimo_puesto'] else '-':<20} "
              f"{perfil:<15} {c['seniority'] or '-':<10} {c['estado']:<12}")
    
    pausa()


def ver_detalle_candidato(db):
    """Mostrar todos los datos de un candidato + historial"""
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  DETALLE DE CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    # Mostrar datos completos
    print(f"\n{'='*70}")
    print(f"📄 FICHA COMPLETA: {candidato['nombre']}")
    print(f"{'='*70}")
    print(f"ID:          {candidato['id']}")
    print(f"Email:       {candidato['email'] or '-'}")
    print(f"Teléfono:    {candidato['telefono'] or '-'}")
    print(f"LinkedIn:    {candidato['linkedin'] or '-'}")
    print(f"GitHub:      {candidato['github'] or '-'}")
    print(f"📍 Ubicación: {candidato['localizacion'] or '-'} | Remoto: {candidato['remoto'] or '-'}")
    print(f"📅 Incorporación: {candidato['disponibilidad'] or '-'}")
    print(f"🚗 Carnet: {'Sí' if candidato['carnet_conducir'] else 'No'} | Vehículo: {'Sí' if candidato['vehiculo_propio'] else 'No'}")
    
    print(f"\n🎓 Formación:")
    print(f"   Estudios:    {candidato['nivel_estudios'] or '-'}")
    print(f"   Titulación:  {candidato['titulacion'] or '-'}")
    print(f"   Certificaciones: {candidato['certificaciones'] or '-'}")
    print(f"   Idiomas:     {candidato['idiomas'] or '-'}")
    
    print(f"\n💼 Experiencia:")
    print(f"   Total IT:    {candidato['experiencia_total']} años")
    print(f"   Telecom:     {candidato['experiencia_telecom']} años")
    print(f"   Último puesto: {candidato['ultimo_puesto'] or '-'} en {candidato['ultima_empresa'] or '-'}")
    print(f"   TM Forum/ODA: {candidato['experiencia_tmforum'] or 'Sin experiencia'}")
    print(f"   Proyectos:   {candidato['proyectos'] or '-'}")
    
    print(f"\n🛠️  Stack técnico:")
    print(f"   Lenguajes:   {candidato['stack_lenguajes'] or '-'}")
    print(f"   Frameworks:  {candidato['stack_frameworks'] or '-'}")
    print(f"   BBDD:        {candidato['stack_bbdd'] or '-'}")
    print(f"   Cloud:       {candidato['stack_cloud'] or '-'}")
    print(f"   DevOps:      {candidato['stack_devops'] or '-'}")
    print(f"   APIs:        {candidato['stack_apis'] or '-'}")
    print(f"   Mensajería:  {candidato['stack_mensajeria'] or '-'}")
    
    print(f"\n🌟 Competencias: {candidato['competencias'] or '-'}")
    
    print(f"\n💰 Salario esperado: {candidato['salario_esperado'] or '-'}")
    print(f"👤 Perfil IT: {PERFILES_IT.get(candidato['perfil_it'], candidato['perfil_it'] or '-')}")
    print(f"⭐ Seniority: {SENIORITY_NIVELES.get(candidato['seniority'], candidato['seniority'] or '-')}")
    
    print(f"\n📝 Notas:")
    print(f"   {candidato['notas'] or '-'}")
    
    print(f"\n🛡️  GDPR: {'✅ Consentimiento registrado' if candidato['gdpr_consent'] else '⚠️  Pendiente'}")
    print(f"📅 Registro:  {candidato['fecha_registro']}")
    print(f"🔍 Origen:     {candidato['origen']}")
    print(f"🏷️  Estado:    {candidato['estado']}")
    
    # Mostrar historial de interacciones
    print(f"\n{'='*70}")
    print("📞 HISTORIAL DE INTERACCIONES")
    print(f"{'='*70}")
    
    interacciones = db.obtener_interacciones(cid)
    
    if not interacciones:
        print("📭 Sin interacciones registradas aún.")
    else:
        for i in interacciones:
            print(f"\n[{i['fecha']}] {i['tipo'].upper()}")
            print(f"   Responsable: {i['responsable'] or '-'}")
            print(f"   Notas: {i['notas']}")
            if i['proximo_paso']:
                print(f"   ➤ Próximo paso: {i['proximo_paso']}")
    
    # Mostrar evaluaciones R/S/T
    print(f"\n{'='*70}")
    print("📊 EVALUACIONES R/S/T")
    print(f"{'='*70}")
    
    evaluaciones = db.obtener_evaluaciones_candidato(cid)
    
    if not evaluaciones:
        print("📭 Sin evaluaciones registradas aún.")
    else:
        for e in evaluaciones:
            print(f"\n[{e['fecha']}] Evaluador: {e['evaluador']}")
            print(f"   R (Comunicación): {e['r_puntuacion']}/10")
            print(f"   S (Técnica):      {e['s_puntuacion']}/10")
            print(f"   T (Cultural):     {e['t_puntuacion']}/10")
            print(f"   ➤ Score final:    {e['score_final']}")
            print(f"   Recomendación:    {e['recomendacion']}")
            if e['senales_encaje']:
                print(f"   ✅ Señales: {e['senales_encaje']}")
    
    pausa()


def editar_candidato(db):
    """Editar campos específicos de un candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   ✏️  EDITAR CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    print("\n¿Qué campo quieres editar?")
    print("  1. Estado")
    print("  2. Notas")
    print("  3. Teléfono/Email")
    print("  4. Stack técnico")
    print("  5. Salario esperado")
    print("  6. Perfil IT/Seniority")
    
    campo_opcion = input("\nOpción (1-6): ").strip()
    
    actualizaciones = {}
    
    if campo_opcion == "1":
        print("\nEstados válidos: activo | screening | entrevista_tecnica | entrevista_hm | finalista | offer | contratado | descartado")
        actualizaciones['estado'] = input("Nuevo estado: ").strip().lower() or 'screening'
    elif campo_opcion == "2":
        actualizaciones['notas'] = input("Nuevas notas: ").strip()
    elif campo_opcion == "3":
        actualizaciones['telefono'] = input(f"Teléfono [{candidato['telefono']}]: ").strip() or candidato['telefono']
        actualizaciones['email'] = input(f"Email [{candidato['email']}]: ").strip() or candidato['email']
    elif campo_opcion == "4":
        actualizaciones['stack_lenguajes'] = input(f"Lenguajes [{candidato['stack_lenguajes']}]: ").strip() or candidato['stack_lenguajes']
        actualizaciones['stack_frameworks'] = input(f"Frameworks [{candidato['stack_frameworks']}]: ").strip() or candidato['stack_frameworks']
    elif campo_opcion == "5":
        actualizaciones['salario_esperado'] = input(f"Salario esperado [{candidato['salario_esperado']}]: ").strip() or candidato['salario_esperado']
    elif campo_opcion == "6":
        print("\nPerfiles IT:")
        for key, value in PERFILES_IT.items():
            print(f"  {key:20} - {value}")
        actualizaciones['perfil_it'] = input(f"Perfil IT [{candidato['perfil_it']}]: ").strip().lower() or candidato['perfil_it']
        
        print("\nSeniority:")
        for key, value in SENIORITY_NIVELES.items():
            print(f"  {key:10} - {value}")
        actualizaciones['seniority'] = input(f"Seniority [{candidato['seniority']}]: ").strip().lower() or candidato['seniority']
    else:
        print("\n⚠️  Opción no válida.")
        pausa()
        return
    
    if db.actualizar_candidato(cid, actualizaciones):
        print("\n✅ Candidato actualizado correctamente.")
    else:
        print("\n❌ Error al actualizar.")
    
    pausa()


def registrar_interaccion(db):
    """Registrar una llamada, email o entrevista con un candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   📞 REGISTRAR INTERACCIÓN")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    
    print("\nTipos de interacción:")
    print("  1. Llamada telefónica")
    print("  2. Email")
    print("  3. Entrevista técnica")
    print("  4. Entrevista cultural/HM")
    print("  5. Offer")
    print("  6. Otra")
    
    tipo_map = {
        "1": "llamada",
        "2": "email",
        "3": "entrevista_tecnica",
        "4": "entrevista_hm",
        "5": "offer",
        "6": "otra"
    }
    
    tipo_opcion = input("\nTipo (1-6): ").strip()
    tipo = tipo_map.get(tipo_opcion, "otra")
    
    responsable = input("Responsable de RRHH: ").strip()
    notas = input("Notas de la interacción: ").strip()
    proximo_paso = input("Próximo paso (opcional): ").strip()
    
    db.agregar_interaccion(cid, tipo, responsable, notas, proximo_paso)
    
    print("\n✅ Interacción registrada correctamente.")
    pausa()


def archivar_candidato(db):
    """Archivar (no borrar) un candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   🗑️  ARCHIVAR CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    confirmar = input("\n⚠️  ¿Confirmas archivar este candidato? (S/n): ").strip().lower()
    
    if confirmar in ('s', 'si', 'y', 'yes', ''):
        if db.eliminar_candidato(cid):
            print("\n✅ Candidato archivado correctamente.")
        else:
            print("\n❌ Error al archivar.")
    else:
        print("\nℹ️  Operación cancelada.")
    
    pausa()


# ========================================
# MENÚ VACANTES
# ========================================

def menu_vacantes(db):
    """Menú de gestión de vacantes"""
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   💼 GESTIÓN DE VACANTES")
        print("=" * 70)
        print("\n1. ➕ Crear nueva vacante")
        print("2. 📋 Listar vacantes")
        print("3. 👁️  Ver detalle de vacante")
        print("4. 🔒 Cerrar vacante (cubierta/cancelada)")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-4): ").strip()
        
        if opcion == "1":
            crear_vacante(db)
        elif opcion == "2":
            listar_vacantes(db)
        elif opcion == "3":
            ver_detalle_vacante(db)
        elif opcion == "4":
            cerrar_vacante(db)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def crear_vacante(db):
    """Formulario para crear nueva vacante"""
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
    while not datos['perfil_it'] in PERFILES_IT:
        print("⚠️  Perfil no válido. Elige uno de la lista.")
        datos['perfil_it'] = input("Perfil IT*: ").strip().lower()
    
    print("\nSeniority:")
    for key, value in SENIORITY_NIVELES.items():
        print(f"  {key:10} - {value}")
    datos['seniority'] = input("\nSeniority*: ").strip().lower()
    while not datos['seniority'] in SENIORITY_NIVELES:
        print("⚠️  Seniority no válido. Elige uno de la lista.")
        datos['seniority'] = input("Seniority*: ").strip().lower()
    
    datos['departamento'] = input("Departamento (Desarrollo/DevOps/Producto/Arquitectura/Operaciones): ").strip()
    datos['ubicacion'] = input("Ubicación (Madrid/Avilés/Remoto): ").strip()
    datos['modalidad'] = input("Modalidad (Remoto_Total/Remoto_Parcial/Presencial): ").strip()
    
    print("\n--- Requisitos técnicos ---")
    datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    while not datos['stack_obligatorio']:
        print("⚠️  El stack obligatorio es obligatorio")
        datos['stack_obligatorio'] = input("Stack obligatorio*: ").strip()
    
    datos['stack_deseable'] = input("Stack deseable: ").strip()
    datos['experiencia_tmforum'] = input("Experiencia TM Forum/ODA (Obligatorio/Deseable/No_relevante): ").strip()
    datos['experiencia_telecom'] = input("Experiencia Telecom OSS/BSS (Obligatorio/Deseable/No_relevante): ").strip()
    datos['certificaciones_requeridas'] = input("Certificaciones requeridas: ").strip()
    
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
    
    datos['tipo_contrato'] = input("Tipo de contrato (Indefinido/Temporal): ").strip()
    datos['jornada'] = input("Jornada (Completa/Parcial): ").strip()
    datos['necesidad'] = input("Tipo de necesidad (Nueva/Reemplazo): ").strip()
    
    print("\n--- Stakeholders ---")
    datos['responsable_seleccion'] = input("Responsable de selección (RRHH)*: ").strip()
    while not datos['responsable_seleccion']:
        print("⚠️  El responsable es obligatorio")
        datos['responsable_seleccion'] = input("Responsable de selección (RRHH)*: ").strip()
    
    datos['responsable_tecnico'] = input("Responsable técnico (Tech Lead/Arquitecto): ").strip()
    datos['hiring_manager'] = input("Hiring Manager (Jefe de Área): ").strip()
    
    datos['fecha_cierre_estimada'] = input("\nFecha cierre estimada (YYYY-MM-DD, opcional): ").strip()
    datos['notas'] = input("Notas adicionales: ").strip()
    
    # Guardar en BD
    vacante_id = db.crear_vacante(datos)
    
    print(f"\n✅ Vacante creada correctamente")
    print(f"   ID: {vacante_id}")
    print(f"   Puesto: {datos['titulo']}")
    print(f"   Perfil: {PERFILES_IT[datos['perfil_it']]} ({datos['seniority'].upper()})")
    
    pausa()


def listar_vacantes(db):
    """Listar vacantes con filtros"""
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 LISTAR VACANTES")
    print("=" * 70)
    
    estado = input("\nFiltrar por estado (abierta/cerrada_cubierta/cerrada_cancelada) - Deja en blanco para todas: ").strip().lower() or None
    
    print("\nPerfiles IT disponibles:")
    for key, value in PERFILES_IT.items():
        print(f"  {key:20} - {value}")
    perfil_filtro = input("\nFiltrar por perfil IT (deja en blanco para todos): ").strip().lower() or None
    
    vacantes = db.listar_vacantes(estado=estado, perfil_it=perfil_filtro)
    
    if not vacantes:
        print("\n📭 No hay vacantes con esos criterios.")
        pausa()
        return
    
    print(f"\n📊 Encontradas: {len(vacantes)} vacantes\n")
    print(f"{'ID':<15} {'Título':<30} {'Perfil':<20} {'Ubicación':<15} {'Estado':<15}")
    print("-" * 95)
    
    for v in vacantes:
        perfil = PERFILES_IT.get(v['perfil_it'], v['perfil_it'])[:20]
        print(f"{v['id']:<15} {v['titulo'][:28]:<30} {perfil:<20} {v['ubicacion'] or '-':<15} {v['estado']:<15}")
    
    pausa()


def ver_detalle_vacante(db):
    """Ver detalle completo de una vacante + candidatos asociados"""
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  DETALLE DE VACANTE")
    print("=" * 70)
    
    vid = input("\nID de la vacante: ").strip()
    vacante = db.obtener_vacante(vid)
    
    if not vacante:
        print("\n❌ Vacante no encontrada.")
        pausa()
        return
    
    # Mostrar datos completos
    print(f"\n{'='*70}")
    print(f"💼 VACANTE: {vacante['titulo']}")
    print(f"{'='*70}")
    print(f"ID:          {vacante['id']}")
    print(f"Perfil:      {PERFILES_IT.get(vacante['perfil_it'], vacante['perfil_it'])}")
    print(f"Seniority:   {SENIORITY_NIVELES.get(vacante['seniority'], vacante['seniority'])}")
    print(f"Departamento:{vacante['departamento'] or '-'}")
    print(f"Ubicación:   {vacante['ubicacion'] or '-'} | Modalidad: {vacante['modalidad'] or '-'}")
    
    print(f"\n🛠️  Requisitos técnicos:")
    print(f"   Obligatorio: {vacante['stack_obligatorio']}")
    print(f"   Deseable:    {vacante['stack_deseable'] or '-'}")
    print(f"   TM Forum/ODA: {vacante['experiencia_tmforum'] or '-'}")
    print(f"   Telecom OSS/BSS: {vacante['experiencia_telecom'] or '-'}")
    print(f"   Certificaciones: {vacante['certificaciones_requeridas'] or '-'}")
    
    print(f"\n💶 Condiciones:")
    print(f"   Salario: {vacante['rango_salarial_min']}k - {vacante['rango_salarial_max']}k €")
    print(f"   Contrato: {vacante['tipo_contrato'] or '-'} | Jornada: {vacante['jornada'] or '-'}")
    print(f"   Necesidad: {vacante['necesidad'] or '-'}")
    
    print(f"\n👥 Stakeholders:")
    print(f"   RRHH:        {vacante['responsable_seleccion']}")
    print(f"   Técnico:     {vacante['responsable_tecnico'] or '-'}")
    print(f"   Hiring Mgr:  {vacante['hiring_manager'] or '-'}")
    
    print(f"\n📅 Cronograma:")
    print(f"   Apertura:    {vacante['fecha_apertura']}")
    print(f"   Cierre est.: {vacante['fecha_cierre_estimada'] or '-'}")
    print(f"   Cierre real: {vacante['fecha_cierre_real'] or '-'}")
    
    print(f"\n📊 KPIs:")
    print(f"   Estado:      {vacante['estado']}")
    print(f"   Candidatos:  {vacante['candidatos_totales']}")
    print(f"   Finalistas:  {vacante['candidatos_finalistas']}")
    print(f"   Seleccionado:{vacante['candidato_seleccionado'] or '-'}")
    if vacante['time_to_hire']:
        print(f"   Time to Hire:{vacante['time_to_hire']} días")
    
    print(f"\n📝 Notas:")
    print(f"   {vacante['notas'] or '-'}")
    
    # Mostrar candidatos asociados
    print(f"\n{'='*70}")
    print("👥 CANDIDATOS ASOCIADOS")
    print(f"{'='*70}")
    
    candidatos = db.obtener_candidatos_vacante(vid)
    
    if not candidatos:
        print("📭 Sin candidatos asociados aún.")
    else:
        print(f"\nTotal: {len(candidatos)} candidatos\n")
        print(f"{'Nombre':<25} {'Fase':<20} {'Score':<10} {'Última actualización':<20}")
        print("-" * 75)
        
        for c in candidatos:
            # Obtener última evaluación para score
            eval_last = db.obtener_ultima_evaluacion(c['id'], vid)
            score = f"{eval_last['score_final']}" if eval_last else "-"
            
            print(f"{c['nombre'][:23]:<25} {c['fase']:<20} {score:<10} {c['fecha_asignacion'][:16]:<20}")
    
    pausa()


def cerrar_vacante(db):
    """Cerrar una vacante (cubierta o cancelada)"""
    limpiar_pantalla()
    print("=" * 70)
    print("   🔒 CERRAR VACANTE")
    print("=" * 70)
    
    vid = input("\nID de la vacante: ").strip()
    vacante = db.obtener_vacante(vid)
    
    if not vacante:
        print("\n❌ Vacante no encontrada.")
        pausa()
        return
    
    print(f"\nVacante: {vacante['titulo']}")
    print(f"Estado actual: {vacante['estado']}")
    
    print("\n¿Cómo cerrar la vacante?")
    print("  1. Cubierta (seleccionado candidato)")
    print("  2. Cancelada (necesidad desaparecida)")
    
    opcion = input("\nOpción (1-2): ").strip()
    
    if opcion == "1":
        cid = input("ID del candidato seleccionado: ").strip()
        candidato = db.obtener_candidato(cid)
        
        if not candidato:
            print("\n❌ Candidato no encontrado.")
            pausa()
            return
        
        confirmar = input(f"\n⚠️  ¿Confirmas cerrar la vacante con {candidato['nombre']}? (S/n): ").strip().lower()
        if confirmar in ('s', 'si', 'y', 'yes', ''):
            # Calcular time_to_hire
            from datetime import datetime as dt
            fecha_apertura = dt.strptime(vacante['fecha_apertura'], "%Y-%m-%d")
            dias = (dt.now() - fecha_apertura).days
            
            db.actualizar_vacante(vid, {'time_to_hire': dias, 'candidatos_finalistas': 1})
            db.cerrar_vacante(vid, cid)
            db.actualizar_candidato(cid, {'estado': 'contratado'})
            
            print("\n✅ Vacante cerrada como CUBIERTA.")
            print(f"   Time to Hire: {dias} días")
    elif opcion == "2":
        confirmar = input("\n⚠️  ¿Confirmas CANCELAR esta vacante? (S/n): ").strip().lower()
        if confirmar in ('s', 'si', 'y', 'yes', ''):
            db.cerrar_vacante(vid)
            print("\n✅ Vacante cerrada como CANCELADA.")
    else:
        print("\nℹ️  Operación cancelada.")
    
    pausa()


# ========================================
# MENÚ EVALUACIONES R/S/T
# ========================================

def menu_evaluaciones(db):
    """Menú de evaluaciones R/S/T"""
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📊 EVALUACIONES R/S/T - Sistema Alvatross")
        print("=" * 70)
        print("\n1. ➕ Nueva evaluación")
        print("2. 📋 Ver historial de evaluaciones")
        print("3. 👁️  Última evaluación de candidato")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-3): ").strip()
        
        if opcion == "1":
            crear_evaluacion(db)
        elif opcion == "2":
            historial_evaluaciones(db)
        elif opcion == "3":
            ultima_evaluacion(db)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def crear_evaluacion(db):
    """Formulario para crear evaluación R/S/T"""
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ NUEVA EVALUACIÓN R/S/T")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    print(f"Perfil: {PERFILES_IT.get(candidato['perfil_it'], candidato['perfil_it'])}")
    
    vid = input("\nID de la vacante (opcional): ").strip()
    if vid:
        vacante = db.obtener_vacante(vid)
        if not vacante:
            print("⚠️  Vacante no encontrada. Continuando sin asociar.")
            vid = None
        else:
            print(f"Vacante: {vacante['titulo']}")
    
    datos = {}
    datos['candidato_id'] = cid
    datos['vacante_id'] = vid if vid else None
    datos['evaluador'] = input("\nEvaluador (tu nombre): ").strip()
    
    print("\n--- Dimensión R: Entrevista/Comunicación (1-10) ---")
    print("   1-3: respuestas vagas, sin ejemplos, confusión conceptos")
    print("   4-6: base correcta, algunos ejemplos, huecos puntuales")
    print("   7-8: sólido, ejemplos claros, buena toma decisiones")
    print("   9-10: excelente, liderazgo/ownership, profundidad")
    try:
        datos['r_puntuacion'] = int(input("Puntuación R (1-10)*: ").strip())
    except ValueError:
        datos['r_puntuacion'] = 0
    
    datos['r_notas'] = input("Notas R: ").strip()
    
    print("\n--- Dimensión S: Técnica/Stack (1-10) ---")
    try:
        datos['s_puntuacion'] = int(input("Puntuación S (1-10)*: ").strip())
    except ValueError:
        datos['s_puntuacion'] = 0
    
    datos['s_notas'] = input("Notas S: ").strip()
    
    print("\n--- Dimensión T: Cultural/Soft Skills (1-10) ---")
    print("   Alineación DevSecOps, colaboración, estabilidad, claridad")
    try:
        datos['t_puntuacion'] = int(input("Puntuación T (1-10)*: ").strip())
    except ValueError:
        datos['t_puntuacion'] = 0
    
    datos['t_notas'] = input("Notas T: ").strip()
    
    # Calcular score final automáticamente
    perfil = candidato['perfil_it'] or 'backend'
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
    score = round((datos['r_puntuacion'] * p_r) + (datos['s_puntuacion'] * p_s) + (datos['t_puntuacion'] * p_t), 2)
    
    print(f"\n➤ Score final calculado: {score}/10")
    
    print("\n--- Señales de buen encaje ---")
    senales = []
    if perfil == 'backend':
        senales.append("Explica decisiones técnicas con datos")
        senales.append("Piensa en resiliencia (timeouts/retries)")
        senales.append("Conoce prácticas calidad (tests/code review)")
    elif perfil == 'devops':
        senales.append("Automatiza por defecto (IaC, pipelines)")
        senales.append("Enfoca seguridad sin bloquear entregas")
    elif perfil == 'qa':
        senales.append("Pensamiento crítico y precisión")
        senales.append("Colabora como habilitador (no policía)")
    
    if senales:
        print("Checklist (marca las que apliquen):")
        for i, senal in enumerate(senales, 1):
            if input(f"  [{i}] {senal} (S/n): ").strip().lower() in ('s', 'si', 'y', 'yes', ''):
                datos.setdefault('senales_encaje', []).append(senal)
        if 'senales_encaje' in datos:
            datos['senales_encaje'] = " | ".join(datos['senales_encaje'])
    
    print("\n--- Recomendación final ---")
    print("  1. Contratar")
    print("  2. Reservas (seguir evaluando)")
    print("  3. Siguiente fase")
    print("  4. Descartar")
    rec_map = {"1": "contratar", "2": "reservas", "3": "siguiente_fase", "4": "descartar"}
    rec_opcion = input("Opción (1-4): ").strip()
    datos['recomendacion'] = rec_map.get(rec_opcion, "reservas")
    
    datos['perfil_it'] = perfil
    
    # Guardar evaluación
    eval_id = db.crear_evaluacion(datos)
    
    print(f"\n✅ Evaluación registrada correctamente")
    print(f"   ID: {eval_id}")
    print(f"   Score final: {score}/10")
    print(f"   Recomendación: {datos['recomendacion']}")
    
    # Actualizar fase en vacante si aplica
    if vid and score >= 7.0:
        db.actualizar_fase_candidato(cid, vid, 'entrevista_tecnica', f"Score R/S/T: {score}")
        print("   ➤ Candidato avanzado a fase 'entrevista_tecnica'")
    
    pausa()


def historial_evaluaciones(db):
    """Ver historial de evaluaciones de un candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 HISTORIAL DE EVALUACIONES")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    evaluaciones = db.obtener_evaluaciones_candidato(cid)
    
    if not evaluaciones:
        print(f"\n📭 {candidato['nombre']} no tiene evaluaciones registradas.")
        pausa()
        return
    
    print(f"\n📊 Evaluaciones de {candidato['nombre']}: {len(evaluaciones)}\n")
    
    for e in evaluaciones:
        print(f"[{e['fecha']}] Evaluador: {e['evaluador']}")
        print(f"   R: {e['r_puntuacion']}/10 | S: {e['s_puntuacion']}/10 | T: {e['t_puntuacion']}/10")
        print(f"   ➤ Score: {e['score_final']} | Recomendación: {e['recomendacion']}")
        if e['senales_encaje']:
            print(f"   ✅ {e['senales_encaje']}")
        print("-" * 70)
    
    pausa()


def ultima_evaluacion(db):
    """Ver última evaluación de un candidato"""
    limpiar_pantalla()
    print("=" * 70)
    print("   👁️  ÚLTIMA EVALUACIÓN")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    vid = input("ID de vacante (opcional, Enter para última general): ").strip() or None
    
    evaluacion = db.obtener_ultima_evaluacion(cid, vid)
    
    if not evaluacion:
        print(f"\n📭 {candidato['nombre']} no tiene evaluaciones.")
        pausa()
        return
    
    print(f"\n📄 Última evaluación de {candidato['nombre']}")
    print(f"Fecha: {evaluacion['fecha']}")
    print(f"Evaluador: {evaluacion['evaluador']}")
    print(f"\nR (Comunicación): {evaluacion['r_puntuacion']}/10")
    print(f"   {evaluacion['r_notas'] or '-'}")
    print(f"\nS (Técnica): {evaluacion['s_puntuacion']}/10")
    print(f"   {evaluacion['s_notas'] or '-'}")
    print(f"\nT (Cultural): {evaluacion['t_puntuacion']}/10")
    print(f"   {evaluacion['t_notas'] or '-'}")
    print(f"\n➤ Score final: {evaluacion['score_final']}/10")
    print(f"Recomendación: {evaluacion['recomendacion']}")
    if evaluacion['senales_encaje']:
        print(f"\n✅ Señales de encaje:\n   {evaluacion['senales_encaje']}")
    
    pausa()


# ========================================
# MENÚ ASOCIACIONES
# ========================================

def menu_asociaciones(db):
    """Menú para asociar candidatos a vacantes"""
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   🔄 ASOCIAR CANDIDATO-VACANTE")
        print("=" * 70)
        print("\n1. ➕ Asociar candidato a vacante")
        print("2. 🔄 Actualizar fase de candidato")
        print("3. 📋 Candidatos por vacante")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-3): ").strip()
        
        if opcion == "1":
            asociar_candidato_vacante(db)
        elif opcion == "2":
            actualizar_fase_candidato(db)
        elif opcion == "3":
            candidatos_por_vacante(db)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def asociar_candidato_vacante(db):
    """Asociar candidato a vacante"""
    limpiar_pantalla()
    print("=" * 70)
    print("   ➕ ASOCIAR CANDIDATO A VACANTE")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    vid = input("ID de la vacante: ").strip()
    vacante = db.obtener_vacante(vid)
    
    if not vacante:
        print("\n❌ Vacante no encontrada.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    print(f"Vacante: {vacante['titulo']}")
    
    fase = input("\nFase inicial (screening/entrevista_tecnica/entrevista_hm/finalista): ").strip() or 'screening'
    notas = input("Notas de la asociación: ").strip()
    
    if db.asociar_candidato_vacante(cid, vid, fase, notas):
        print("\n✅ Candidato asociado correctamente a la vacante.")
        print(f"   Fase inicial: {fase}")
    else:
        print("\n❌ Error al asociar.")
    
    pausa()


def actualizar_fase_candidato(db):
    """Actualizar fase de candidato en vacante"""
    limpiar_pantalla()
    print("=" * 70)
    print("   🔄 ACTUALIZAR FASE DE CANDIDATO")
    print("=" * 70)
    
    cid = input("\nID del candidato: ").strip()
    vid = input("ID de la vacante: ").strip()
    
    print("\nFases disponibles:")
    print("  screening | entrevista_tecnica | entrevista_hm | finalista | offer | contratado | descartado")
    
    nueva_fase = input("\nNueva fase: ").strip()
    notas = input("Notas de la actualización: ").strip()
    
    if db.actualizar_fase_candidato(cid, vid, nueva_fase, notas):
        print("\n✅ Fase actualizada correctamente.")
        print(f"   Nueva fase: {nueva_fase}")
    else:
        print("\n❌ Error al actualizar fase.")
    
    pausa()


def candidatos_por_vacante(db):
    """Listar candidatos asociados a una vacante"""
    limpiar_pantalla()
    print("=" * 70)
    print("   📋 CANDIDATOS POR VACANTE")
    print("=" * 70)
    
    vid = input("\nID de la vacante: ").strip()
    vacante = db.obtener_vacante(vid)
    
    if not vacante:
        print("\n❌ Vacante no encontrada.")
        pausa()
        return
    
    print(f"\nVacante: {vacante['titulo']}")
    print(f"Estado: {vacante['estado']}")
    
    fase = input("\nFiltrar por fase (deja en blanco para todas): ").strip() or None
    
    candidatos = db.obtener_candidatos_vacante(vid, fase)
    
    if not candidatos:
        print("\n📭 Sin candidatos en esta fase.")
        pausa()
        return
    
    print(f"\n📊 Candidatos: {len(candidatos)}\n")
    print(f"{'Nombre':<25} {'Fase':<20} {'Stack':<30} {'Score':<10}")
    print("-" * 80)
    
    for c in candidatos:
        # Obtener última evaluación para score
        eval_last = db.obtener_ultima_evaluacion(c['id'], vid)
        score = f"{eval_last['score_final']}" if eval_last else "-"
        stack = c['stack_lenguajes'][:28] + "..." if c['stack_lenguajes'] and len(c['stack_lenguajes']) > 28 else (c['stack_lenguajes'] or "-")
        
        print(f"{c['nombre'][:23]:<25} {c['fase']:<20} {stack:<30} {score:<10}")
    
    pausa()


# ========================================
# MENÚ EXPORTACIÓN
# ========================================

def menu_exportacion(db):
    """Menú de exportación de datos"""
    while True:
        limpiar_pantalla()
        print("=" * 70)
        print("   📤 EXPORTAR DATOS")
        print("=" * 70)
        print("\n1. 📄 Exportar candidatos a CSV")
        print("2. 💼 Exportar vacantes a CSV")
        print("0. ⬅️  Volver al menú principal")
        print("-" * 70)
        
        opcion = input("\n➤ Elige una opción (0-2): ").strip()
        
        if opcion == "1":
            exportar_candidatos_csv(db)
        elif opcion == "2":
            exportar_vacantes_csv(db)
        elif opcion == "0":
            break
        else:
            print("\n⚠️  Opción no válida.")
            pausa()


def exportar_candidatos_csv(db):
    """Exportar candidatos a CSV"""
    limpiar_pantalla()
    print("=" * 70)
    print("   📄 EXPORTAR CANDIDATOS A CSV")
    print("=" * 70)
    
    nombre = input("\nNombre del archivo (por defecto: candidatos_export.csv): ").strip()
    if not nombre:
        nombre = "candidatos_export.csv"
    
    if db.exportar_csv_candidatos(nombre):
        print(f"\n✅ Exportado correctamente a: {nombre}")
        print(f"   Ruta completa: {os.path.abspath(nombre)}")
    else:
        print("\n❌ Error al exportar o no hay candidatos.")
    
    pausa()


def exportar_vacantes_csv(db):
    """Exportar vacantes a CSV"""
    limpiar_pantalla()
    print("=" * 70)
    print("   💼 EXPORTAR VACANTES A CSV")
    print("=" * 70)
    
    nombre = input("\nNombre del archivo (por defecto: vacantes_export.csv): ").strip()
    if not nombre:
        nombre = "vacantes_export.csv"
    
    if db.exportar_csv_vacantes(nombre):
        print(f"\n✅ Exportado correctamente a: {nombre}")
        print(f"   Ruta completa: {os.path.abspath(nombre)}")
    else:
        print("\n❌ Error al exportar o no hay vacantes.")
    
    pausa()


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    # Crear carpeta data si no existe
    if not os.path.exists("data"):
        print("📁 Creando carpeta 'data' para la base de datos...")
        os.makedirs("data", exist_ok=True)
    
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
