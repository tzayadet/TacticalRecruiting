#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Menú principal de la app RRHH Alvatross
"""

from database import DatabaseManager
from datetime import datetime
import os
import sys


def limpiar_pantalla():
    """Limpia la terminal (funciona en Windows y Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    """Pausa hasta que el usuario pulse Enter"""
    input("\n↲ Pulsa Enter para continuar...")


def menu_principal():
    """Menú principal de la aplicación"""
    db = DatabaseManager()
    
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("   📋 APP RRHH ALVATROSS - Módulo Candidatos")
        print("=" * 60)
        print("\n1. 🆕 Registrar nuevo candidato")
        print("2. 🔍 Buscar/listar candidatos")
        print("3. 👁️  Ver detalle de candidato")
        print("4. ✏️  Editar candidato")
        print("5. 📞 Registrar interacción (llamada/email/entrevista)")
        print("6. 📤 Exportar a CSV")
        print("0. ❌ Salir")
        print("-" * 60)
        
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
            exportar_csv(db)
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto! Que el stack te acompañe.")
            db.disconnect()
            break
        else:
            print("\n⚠️  Opción no válida. Inténtalo de nuevo.")
            pausa()


def registrar_candidato(db):
    """Formulario para registrar un nuevo candidato"""
    limpiar_pantalla()
    print("=" * 60)
    print("   🆕 REGISTRAR NUEVO CANDIDATO")
    print("=" * 60)
    print("(Puedes dejar campos en blanco pulsando Enter)")
    
    datos = {}
    
    # Datos obligatorios
    while not datos.get('nombre'):
        datos['nombre'] = input("\nNombre completo*: ").strip()
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
    
    print("\n--- Adjuntos y notas ---")
    datos['cv_path'] = input("Ruta al CV (opcional): ").strip()
    datos['portfolio'] = input("URL portfolio (opcional): ").strip()
    datos['notas'] = input("Notas iniciales: ").strip()
    
    # GDPR
    gdpr = input("\n✅ ¿Consentimiento GDPR registrado? (S/n): ").strip().lower()
    datos['gdpr_consent'] = 1 if gdpr in ('', 's', 'si', 'yes') else 0
    datos['origen'] = "manual"
    
    # Guardar en BD
    candidato_id = db.crear_candidato(datos)
    
    print(f"\n✅ Candidato registrado correctamente")
    print(f"   ID: {candidato_id}")
    print(f"   Nombre: {datos['nombre']}")
    print(f"   Puesto: {datos['ultimo_puesto'] or 'Sin especificar'}")
    
    pausa()


def listar_candidatos(db):
    """Listar candidatos con búsqueda y filtros"""
    limpiar_pantalla()
    print("=" * 60)
    print("   🔍 LISTAR CANDIDATOS")
    print("=" * 60)
    
    buscar = input("\nBuscar (nombre, stack, puesto) - Deja en blanco para mostrar todos: ").strip()
    estado = input("Filtrar por estado (screening/entrevista/offer/descartado) - Deja en blanco para todos: ").strip().lower() or None
    
    candidatos = db.listar_candidatos(filtro_estado=estado, buscar=buscar)
    
    if not candidatos:
        print("\n📭 No se encontraron candidatos con esos criterios.")
        pausa()
        return
    
    print(f"\n📊 Encontrados: {len(candidatos)} candidatos\n")
    print(f"{'ID':<15} {'Nombre':<25} {'Puesto':<25} {'Stack':<30} {'Estado':<12}")
    print("-" * 100)
    
    for c in candidatos:
        stack_resumen = c['stack_lenguajes'][:25] + "..." if c['stack_lenguajes'] and len(c['stack_lenguajes']) > 25 else (c['stack_lenguajes'] or "-")
        print(f"{c['id']:<15} {c['nombre'][:23]:<25} {c['ultimo_puesto'][:23] if c['ultimo_puesto'] else '-':<25} {stack_resumen:<30} {c['estado']:<12}")
    
    pausa()


def ver_detalle_candidato(db):
    """Mostrar todos los datos de un candidato + historial de interacciones"""
    limpiar_pantalla()
    print("=" * 60)
    print("   👁️  DETALLE DE CANDIDATO")
    print("=" * 60)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    # Mostrar datos completos
    print(f"\n{'='*60}")
    print(f"📄 FICHA COMPLETA: {candidato['nombre']}")
    print(f"{'='*60}")
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
    print(f"\n📎 Adjuntos:")
    print(f"   CV:          {candidato['cv_path'] or '-'}")
    print(f"   Portfolio:   {candidato['portfolio'] or '-'}")
    print(f"\n📝 Notas:")
    print(f"   {candidato['notas'] or '-'}")
    print(f"\n🛡️  GDPR: {'✅ Consentimiento registrado' if candidato['gdpr_consent'] else '⚠️  Pendiente'}")
    print(f"📅 Registro:  {candidato['fecha_registro']}")
    print(f"🏷️  Estado:    {candidato['estado']}")
    print(f"🔍 Origen:     {candidato['origen']}")
    
    # Mostrar historial de interacciones
    print(f"\n{'='*60}")
    print("📞 HISTORIAL DE INTERACCIONES")
    print(f"{'='*60}")
    
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
    
    pausa()


def editar_candidato(db):
    """Editar campos específicos de un candidato"""
    limpiar_pantalla()
    print("=" * 60)
    print("   ✏️  EDITAR CANDIDATO")
    print("=" * 60)
    
    cid = input("\nID del candidato: ").strip()
    candidato = db.obtener_candidato(cid)
    
    if not candidato:
        print("\n❌ Candidato no encontrado.")
        pausa()
        return
    
    print(f"\nCandidato: {candidato['nombre']}")
    print("\n¿Qué campo quieres editar?")
    print("  1. Estado (screening/entrevista/offer/descartado)")
    print("  2. Notas")
    print("  3. Teléfono")
    print("  4. Email")
    print("  5. Stack técnico (lenguajes)")
    print("  6. Varios campos (avanzado)")
    
    campo_opcion = input("\nOpción (1-6): ").strip()
    
    actualizaciones = {}
    
    if campo_opcion == "1":
        print("\nEstados válidos: screening | entrevista | offer | descartado | activo")
        actualizaciones['estado'] = input("Nuevo estado: ").strip().lower() or 'screening'
    elif campo_opcion == "2":
        actualizaciones['notas'] = input("Nuevas notas: ").strip()
    elif campo_opcion == "3":
        actualizaciones['telefono'] = input("Nuevo teléfono: ").strip()
    elif campo_opcion == "4":
        actualizaciones['email'] = input("Nuevo email: ").strip()
    elif campo_opcion == "5":
        actualizaciones['stack_lenguajes'] = input("Nuevo stack (lenguajes): ").strip()
    elif campo_opcion == "6":
        print("\n(Edita los campos que quieras. Deja en blanco para no modificar)")
        actualizaciones['telefono'] = input(f"Teléfono [{candidato['telefono']}]: ").strip() or candidato['telefono']
        actualizaciones['email'] = input(f"Email [{candidato['email']}]: ").strip() or candidato['email']
        actualizaciones['estado'] = input(f"Estado [{candidato['estado']}]: ").strip().lower() or candidato['estado']
        actualizaciones['notas'] = input(f"Notas [{candidato['notas'][:50]}...]: ").strip() or candidato['notas']
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
    print("=" * 60)
    print("   📞 REGISTRAR INTERACCIÓN")
    print("=" * 60)
    
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
        "4": "entrevista_cultural",
        "5": "offer",
        "6": "otra"
    }
    
    tipo_opcion = input("\nTipo (1-6): ").strip()
    tipo = tipo_map.get(tipo_opcion, "otra")
    
    responsable = input("Responsable de RRHH: ").strip()
    notas = input("Notas de la interacción: ").strip()
    proximo_paso = input("Próximo paso (opcional): ").strip()
    
    db.agregar_interaccion(cid, tipo, responsable, notas, proximo_paso)
    
    # Actualizar estado automáticamente según tipo
    if tipo == "entrevista_tecnica":
        db.actualizar_candidato(cid, {'estado': 'entrevista'})
    elif tipo == "offer":
        db.actualizar_candidato(cid, {'estado': 'offer'})
    
    print("\n✅ Interacción registrada correctamente.")
    pausa()


def exportar_csv(db):
    """Exportar todos los candidatos a CSV"""
    limpiar_pantalla()
    print("=" * 60)
    print("   📤 EXPORTAR A CSV")
    print("=" * 60)
    
    nombre_archivo = input("\nNombre del archivo (por defecto: candidatos_export.csv): ").strip()
    if not nombre_archivo:
        nombre_archivo = "candidatos_export.csv"
    
    if db.exportar_csv(nombre_archivo):
        print(f"\n✅ Exportado correctamente a: {nombre_archivo}")
        print(f"   Ubicación: {os.path.abspath(nombre_archivo)}")
    else:
        print("\n❌ No hay candidatos para exportar o error al guardar.")
    
    pausa()


if __name__ == "__main__":
    # Verificar que la carpeta data existe
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
