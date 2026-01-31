#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
models.py
Estructuras de datos para RRHH Alvatross - perfiles IT/telecom reales
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class EstadoCandidato(Enum):
    ACTIVO = "activo"
    SCREENING = "screening"
    ENTREVISTA_TECNICA = "entrevista_tecnica"
    ENTREVISTA_HM = "entrevista_hm"
    FINALISTA = "finalista"
    OFFER = "offer"
    CONTRATADO = "contratado"
    DESCARTADO = "descartado"
    ARCHIVADO = "archivado"


class PerfilIT(Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DEVOPS = "devops"
    QA = "qa"
    CLOUD = "cloud"
    INTEGRATIONS = "integrations"
    SOLUTION_ARCHITECT = "solution_architect"
    PRODUCT_OWNER = "product_owner"
    SUPPORT = "support"


class Seniority(Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"


@dataclass
class Candidato:
    id: str
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    localizacion: Optional[str] = None
    remoto: Optional[str] = None  # Total/Parcial/Presencial
    disponibilidad: Optional[str] = None  # Inmediata/15d/30d/60d+
    
    # Formación
    nivel_estudios: Optional[str] = None
    titulacion: Optional[str] = None
    certificaciones: Optional[str] = None
    idiomas: Optional[str] = None
    
    # Experiencia
    experiencia_total: int = 0
    experiencia_telecom: int = 0
    experiencia_tmforum: Optional[str] = None  # Sí/No/Nivel
    ultimo_puesto: Optional[str] = None
    ultima_empresa: Optional[str] = None
    proyectos: Optional[str] = None
    
    # Stack técnico (específico Alvatross)
    stack_lenguajes: Optional[str] = None  # Java, Python, TypeScript...
    stack_frameworks: Optional[str] = None  # Spring Boot, Angular, React...
    stack_bbdd: Optional[str] = None  # Oracle, PostgreSQL, MongoDB...
    stack_cloud: Optional[str] = None  # AWS, Azure, GCP
    stack_devops: Optional[str] = None  # Docker, Kubernetes, Terraform...
    stack_apis: Optional[str] = None  # TMForum OpenAPIs, REST, SOAP...
    stack_mensajeria: Optional[str] = None  # Kafka, RabbitMQ...
    
    # Competencias blandas
    competencias: Optional[str] = None
    
    # RRHH
    salario_esperado: Optional[str] = None
    estado: EstadoCandidato = EstadoCandidato.ACTIVO
    perfil_it: Optional[PerfilIT] = None
    seniority: Optional[Seniority] = None
    
    # GDPR y metadata
    gdpr_consent: bool = False
    fecha_registro: Optional[str] = None
    origen: Optional[str] = None  # LinkedIn/Referido/JobBoard/Manual
    notas: Optional[str] = None


@dataclass
class Vacante:
    id: str  # ALV-2026-001
    titulo: str
    perfil_it: PerfilIT
    seniority: Seniority
    departamento: str
    ubicacion: str  # Madrid/Avilés/Remoto
    modalidad: str  # Remoto_Total/Remoto_Parcial/Presencial
    
    # Requisitos técnicos (específico Alvatross)
    stack_obligatorio: str
    stack_deseable: str
    experiencia_tmforum: str  # Obligatorio/Deseable/No_relevante
    experiencia_telecom: str  # Obligatorio/Deseable/No_relevante
    
    # Contratación
    rango_salarial_min: int
    rango_salarial_max: int
    tipo_contrato: str  # Indefinido/Temporal
    necesidad: str  # Nueva/Reemplazo
    
    # Stakeholders
    responsable_seleccion: str
    responsable_tecnico: str
    hiring_manager: str
    
    # Cronograma
    fecha_apertura: str
    fecha_cierre_estimada: Optional[str] = None
    fecha_cierre_real: Optional[str] = None
    
    # Estado
    estado: str = "abierta"  # abierta/en_proceso/cerrada_cubierta/cerrada_cancelada
    
    # KPIs
    time_to_hire: Optional[int] = None  # días
    candidatos_totales: int = 0
    candidatos_finalistas: int = 0
    candidato_seleccionado: Optional[str] = None  # ID candidato


@dataclass
class EvaluacionRST:
    candidato_id: str
    vacante_id: Optional[str] = None
    
    # Dimensión R: Entrevista/Comunicación (1-10)
    r_puntuacion: int = 0
    r_notas: str = ""
    
    # Dimensión S: Técnica/Stack (1-10)
    s_puntuacion: int = 0
    s_notas: str = ""
    
    # Dimensión T: Cultural/Soft Skills (1-10)
    t_puntuacion: int = 0
    t_notas: str = ""
    
    # Score final calculado
    score_final: float = 0.0
    
    # Señales de buen encaje (checklist por perfil)
    senales_encaje: str = ""
    
    # Metadata
    evaluador: str = ""
    fecha: str = ""
    recomendacion: str = ""  # contratar / reservas / siguiente_fase / descartar
