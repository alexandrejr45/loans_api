from loan_simulation.models.dataclasses import LoanSimulationResponse, User
from loan_simulation.models.loan_simulation import LoanSimulation


def convert_loan_model_to_dataclass(
    loan_simulation: LoanSimulation
) -> LoanSimulationResponse | None:
    if loan_simulation:
        return LoanSimulationResponse(
            id=loan_simulation.simulation_id,
            total_amount=loan_simulation.total_amount,
            total_interest_amount=loan_simulation.total_interest_amount,
            monthly_installment=loan_simulation.monthly_installment,
            user=User(
                name=loan_simulation.user.name,
                last_name=loan_simulation.user.last_name,
                document_number=loan_simulation.user.document_number,
                birthdate=loan_simulation.user.birthdate
            )
        )
    return None
