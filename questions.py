#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
questions.py
Banco de preguntas de entrevista para RRHH Alvatross
Categorizado por: general, técnica (por perfil), cultural, situacional
"""

import sqlite3
from pathlib import Path
from typing import List, Dict


class QuestionBank:
    """Gestor del banco de preguntas de entrevista"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            data_dir = Path(__file__).parent / "data"
            data_dir.mkdir(exist_ok=True)
            self.db_path = data_dir / "rrhh_alvatross.db"
        else:
            self.db_path = Path(db_path)
        
        self._create_table()
        self._seed_initial_questions()  # Preguntas iniciales Alvatross
    
    def _create_table(self):
        """Crear tabla de preguntas si no existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas_entrevista (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,          -- general|tecnica|cultural|situacional
                subcategoria TEXT,                -- perfil IT específico para técnica
                texto TEXT NOT NULL,
                ejemplo_respuesta TEXT,
                nivel_dificultad TEXT,            -- facil|medio|dificil
                tags TEXT,                        -- palabras clave para búsqueda
                creada_por TEXT DEFAULT 'sistema',
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para búsqueda rápida
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON preguntas_entrevista(categoria)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_subcategoria ON preguntas_entrevista(subcategoria)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON preguntas_entrevista(tags)')
        
        conn.commit()
        conn.close()
    
    def _seed_initial_questions(self):
        """Sembrar preguntas iniciales específicas de Alvatross (solo si tabla vacía)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existen preguntas
        cursor.execute('SELECT COUNT(*) FROM preguntas_entrevista')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Preguntas iniciales - Alvatross específico
        preguntas_iniciales = [
            # ===== GENERAL =====
            ('general', None, 'Cuéntame tu trayectoria profesional en los últimos 5 años', 
             'Busca narrativa coherente, progresión, motivaciones', 'medio', 'trayectoria,experiencia'),
            ('general', None, '¿Por qué estás interesado en Alvatross/Grupo SATEC?', 
             'Busca conocimiento real de la empresa, no respuesta genérica', 'medio', 'motivación,empresa'),
            ('general', None, '¿Qué sabes de nuestras soluciones OSS/BSS y el stack TM Forum?', 
             'Valida investigación previa sobre el core business', 'dificil', 'oss,bss,tmforum,investigación'),
            
            # ===== CULTURAL =====
            ('cultural', None, 'Describe tu experiencia trabajando en equipos multidisciplinares (devs, QA, arquitectos, producto)', 
             'Busca colaboración real, no solo coexistencia', 'medio', 'colaboración,equipos'),
            ('cultural', None, '¿Cómo manejas los desacuerdos técnicos con compañeros o tech leads?', 
             'Busca madurez, escucha activa, enfoque en solución', 'medio', 'conflicto,resolución'),
            ('cultural', None, 'En Alvatross valoramos proyectos de larga duración con clientes estables. ¿Cómo ves tu evolución profesional a 3-5 años?', 
             'Busca estabilidad vs. job hopping constante', 'medio', 'estabilidad,carrera'),
            ('cultural', None, '¿Cómo explicas decisiones técnicas complejas a perfiles no técnicos (producto, cliente)?', 
             'Busca claridad, empatía, adaptación al interlocutor', 'medio', 'comunicación,empatía'),
            
            # ===== SITUACIONAL =====
            ('situacional', None, 'Estás en mitad de un sprint y descubres un bug crítico en producción. ¿Qué haces?', 
             'Busca protocolo: alerta equipo, rollback si necesario, análisis causa raíz, comunicación', 'dificil', 'crisis,producción,protocolo'),
            ('situacional', None, 'Un compañero critica constantemente tus PRs de forma poco constructiva. ¿Cómo actúas?', 
             'Busca asertividad, canalización por tech lead si persiste, enfoque en mejora', 'medio', 'conflicto,pr'),
            ('situacional', None, 'Te asignan una tarea fuera de tu zona de confort (ej: backend puro si eres full-stack frontend). ¿Cómo afrontas el reto?', 
             'Busca actitud de aprendizaje, petición de recursos/mentoring, ownership', 'medio', 'aprendizaje,adaptación'),
            
            # ===== TÉCNICA: BACKEND =====
            ('tecnica', 'backend', 'En un microservicio Java/Spring Boot, ¿cómo gestionarías la resiliencia ante fallos de dependencias externas?', 
             'Esperamos: circuit breakers (Resilience4j), timeouts, retries con backoff exponencial, fallbacks', 'dificil', 'resiliencia,microservicios,spring'),
            ('tecnica', 'backend', '¿Cómo diseñarías el versionado de APIs REST en un entorno OSS/BSS con múltiples clientes?', 
             'Esperamos: versionado en URL/header, estrategia de deprecated, contrato claro, documentación', 'medio', 'apis,versionado,contrato'),
            ('tecnica', 'backend', '¿Qué patrones aplicarías para evitar N+1 queries en una API que devuelve órdenes con sus líneas?', 
             'Esperamos: JOIN FETCH, EntityGraph, DTO projection, paginación', 'medio', 'optimización,queries,jpa'),
            ('tecnica', 'backend', '¿Cómo garantizarías la idempotencia en una API de provisión de servicios (ej: activar línea móvil)?', 
             'Esperamos: idempotency keys, registro de operaciones, validación previa a ejecución', 'dificil', 'idempotencia,transacciones'),
            
            # ===== TÉCNICA: DEVOPS =====
            ('tecnica', 'devops', '¿Cómo diseñarías un pipeline GitLab CI para un microservicio con requerimientos de seguridad en entornos regulados?', 
             'Esperamos: SAST/DAST en pipeline, escaneo imágenes, firmado artefactos, aprobaciones manuales en prod, secrets management', 'dificil', 'cicd,seguridad,compliance'),
            ('tecnica', 'devops', 'Un despliegue en Kubernetes falla en el 30% de los pods. ¿Cuál es tu proceso de diagnóstico?', 
             'Esperamos: logs pods fallidos, events namespace, describe pod, readiness/liveness probes, recursos asignados', 'medio', 'kubernetes,debugging'),
            ('tecnica', 'devops', '¿Cómo gestionarías el secreto de una API de TM Forum en múltiples entornos sin exponerlo en código?', 
             'Esperamos: Vault/HashiCorp, Kubernetes Secrets con RBAC, variables entorno cifradas, nunca en repositorio', 'dificil', 'secrets,seguridad'),
            
            # ===== TÉCNICA: QA =====
            ('tecnica', 'qa', '¿Cómo estructurarías la estrategia de testing para una API TM Forum Open API (ej: Product Ordering)?', 
             'Esperamos: contrato primero (OpenAPI spec), tests de contrato, happy path + edge cases, idempotencia, concurrencia', 'dificil', 'testing,apis,tmforum'),
            ('tecnica', 'qa', 'Un bug crítico pasa QA y llega a producción. ¿Qué harías tras detectarlo?', 
             'Esperamos: rollback inmediato si posible, análisis causa raíz (¿por qué falló QA?), mejora del proceso, no culpas', 'medio', 'calidad,mejora_continua'),
            
            # ===== TÉCNICA: INTEGRATIONS =====
            ('tecnica', 'integrations', '¿Qué información es crítica en los logs de una integración con un sistema legacy de provisión?', 
             'Esperamos: correlation ID, payload entrada/salida (sanitizado), timestamps, estado transaccional, errores técnicos vs negocio', 'medio', 'logs,integración,debugging'),
            ('tecnica', 'integrations', '¿Cómo manejarías la incompatibilidad de formatos entre una API REST moderna y un sistema SOAP legacy?', 
             'Esperamos: adapter pattern, transformación en middleware, validación contratos, logging exhaustivo', 'dificil', 'integración,legacy,transformación'),
            
            # ===== TÉCNICA: SOLUTION ARCHITECT =====
            ('tecnica', 'solution_architect', 'Un cliente exige alta disponibilidad (99.99%) para su plataforma OSS. ¿Qué elementos arquitectónicos propondrías?', 
             'Esperamos: multi-AZ/region, circuit breakers, rate limiting, cache layers, DB replication, chaos engineering, SLA monitoring', 'dificil', 'arquitectura,ha,escalabilidad'),
            ('tecnica', 'solution_architect', '¿Cómo justificarías técnicamente el uso de ODA (Open Digital Architecture) frente a una arquitectura monolítica legacy?', 
             'Esperamos: agilidad time-to-market, reducción vendor lock-in, interoperabilidad TM Forum, capacidad evolutiva, TCO a largo plazo', 'dificil', 'oda,arquitectura,tmforum'),
            
            # ===== TÉCNICA: PRODUCT OWNER =====
            ('tecnica', 'product_owner', '¿Cómo priorizarías el backlog cuando el equipo tiene capacidad para 10 story points pero hay 30 puntos de demanda de negocio?', 
             'Esperamos: valor vs esfuerzo, RICE framework, alineación con OKRs trimestrales, transparencia con stakeholders', 'medio', 'priorización,backlog'),
            ('tecnica', 'product_owner', 'Un desarrollador dice que una user story es técnicamente inviable. ¿Cuál es tu siguiente paso?', 
             'Esperamos: entender limitación técnica real, buscar alternativas con dev/arquitecto, replantear valor vs solución, no imponer', 'medio', 'colaboración,técnico'),
            
            # ===== TÉCNICA: SUPPORT =====
            ('tecnica', 'support', 'Recibes una alerta: "Tasa de error 5xx en API ProductOrdering > 5%". ¿Cuál es tu protocolo de actuación?', 
             'Esperamos: verificar alerta (no falso positivo), revisar métricas correlacionadas, identificar patrón (hora, cliente, endpoint), escalar a equipo técnico si persiste', 'dificil', 'incidentes,alertas,protocolo'),
            ('tecnica', 'support', 'Un cliente reporta que una orden de servicio está "atascada" en estado PENDING desde hace 2 horas. ¿Cómo investigas?', 
             'Esperamos: buscar order ID en logs, verificar estado en BD, revisar colas de mensajería (Kafka), contactar con equipo de integraciones si necesario', 'medio', 'soporte,debugging,clientes'),
        ]
        
        cursor.executemany('''
            INSERT INTO preguntas_entrevista 
            (categoria, subcategoria, texto, ejemplo_respuesta, nivel_dificultad, tags, creada_por)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', preguntas_iniciales)
        
        conn.commit()
        conn.close()
        print("✅ Banco de preguntas inicializado con preguntas Alvatross específicas")
    
    # ===== CRUD =====
    
    def agregar_pregunta(self, categoria: str, texto: str, subcategoria: str = None, 
                        ejemplo_respuesta: str = None, nivel_dificultad: str = 'medio', 
                        tags: str = None, creada_por: str = 'usuario'):
        """Agregar nueva pregunta al banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO preguntas_entrevista 
            (categoria, subcategoria, texto, ejemplo_respuesta, nivel_dificultad, tags, creada_por)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (categoria, subcategoria, texto, ejemplo_respuesta, nivel_dificultad, tags, creada_por))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def listar_preguntas(self, categoria: str = None, subcategoria: str = None, 
                        buscar: str = None, nivel: str = None) -> List[Dict]:
        """Listar preguntas con filtros"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM preguntas_entrevista WHERE 1=1"
        params = []
        
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        
        if subcategoria:
            query += " AND subcategoria = ?"
            params.append(subcategoria)
        
        if nivel:
            query += " AND nivel_dificultad = ?"
            params.append(nivel)
        
        if buscar:
            query += " AND (texto LIKE ? OR tags LIKE ? OR ejemplo_respuesta LIKE ?)"
            buscar_param = f"%{buscar}%"
            params.extend([buscar_param, buscar_param, buscar_param])
        
        query += " ORDER BY categoria, subcategoria, nivel_dificultad DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def buscar_por_tags(self, tags: List[str]) -> List[Dict]:
        """Buscar preguntas que contengan cualquiera de los tags proporcionados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar preguntas donde tags contenga cualquiera de los términos
        condiciones = " OR ".join(["tags LIKE ?" for _ in tags])
        query = f"SELECT * FROM preguntas_entrevista WHERE {condiciones} ORDER BY categoria"
        params = [f"%{tag}%" for tag in tags]
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in resultados]
    
    def obtener_pregunta(self, pregunta_id: int) -> Dict:
        """Obtener una pregunta por ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM preguntas_entrevista WHERE id = ?', (pregunta_id,))
        resultado = cursor.fetchone()
        conn.close()
        
        return dict(resultado) if resultado else None
    
    def eliminar_pregunta(self, pregunta_id: int) -> bool:
        """Eliminar pregunta (soft delete no implementado, borrado real)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM preguntas_entrevista WHERE id = ?', (pregunta_id,))
        conn.commit()
        exito = cursor.rowcount > 0
        conn.close()
        
        return exito
    
    # ===== UTILIDADES =====
    
    def generar_guia_entrevista(self, perfil_it: str, incluir_cultural: bool = True, 
                               incluir_situacional: bool = True) -> List[Dict]:
        """Generar guía de entrevista personalizada por perfil IT"""
        preguntas = []
        
        # Preguntas técnicas específicas del perfil
        tecnicas = self.listar_preguntas(categoria='tecnica', subcategoria=perfil_it)
        if tecnicas:
            preguntas.append({'seccion': '🎯 TÉCNICAS ESPECÍFICAS', 'preguntas': tecnicas})
        
        # Preguntas generales
        generales = self.listar_preguntas(categoria='general')
        if generales:
            preguntas.append({'seccion': '🗣️ GENERALES', 'preguntas': generales[:3]})  # Top 3
        
        # Preguntas culturales
        if incluir_cultural:
            culturales = self.listar_preguntas(categoria='cultural')
            if culturales:
                preguntas.append({'seccion': '🌟 CULTURALES / ENCAJE', 'preguntas': culturales[:4]})
        
        # Preguntas situacionales
        if incluir_situacional:
            situacionales = self.listar_preguntas(categoria='situacional')
            if situacionales:
                preguntas.append({'seccion': '⚡ SITUACIONALES / COMPORTAMIENTO', 'preguntas': situacionales[:3]})
        
        return preguntas
    
    def estadisticas(self) -> Dict:
        """Obtener estadísticas del banco de preguntas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total por categoría
        cursor.execute('SELECT categoria, COUNT(*) FROM preguntas_entrevista GROUP BY categoria')
        stats['por_categoria'] = dict(cursor.fetchall())
        
        # Total por perfil técnico
        cursor.execute('SELECT subcategoria, COUNT(*) FROM preguntas_entrevista WHERE categoria="tecnica" AND subcategoria IS NOT NULL GROUP BY subcategoria')
        stats['por_perfil'] = dict(cursor.fetchall())
        
        # Total general
        cursor.execute('SELECT COUNT(*) FROM preguntas_entrevista')
        stats['total'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
