#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Menú principal de la app RRHH Alvatross
Incluye: gestión candidatos, vacantes, evaluaciones R/S/T, perfiles IT específicos
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
