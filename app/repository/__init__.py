from app.repository.sqlaRepository import SqlalchemyRepository

from app import models

StudentRepository = SqlalchemyRepository[models.Students](models.Students)
ProfessorRepository = SqlalchemyRepository[models.Professors](models.Professors)
StructuralUnitRepository = SqlalchemyRepository[models.StructuralUnits](models.StructuralUnits)
EmploymentRepository = SqlalchemyRepository[models.Employments](models.Employments)
FieldRepository = SqlalchemyRepository[models.Fields](models.Fields)
StudentsGroupRepository = SqlalchemyRepository[models.StudentsGroups](models.StudentsGroups)
FieldComprehensionRepository = SqlalchemyRepository[models.FieldComprehensions](models.FieldComprehensions)
StudentIdRepository = SqlalchemyRepository[models.StudentIds](models.StudentIds)
