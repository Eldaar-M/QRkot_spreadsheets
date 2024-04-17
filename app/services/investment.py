from datetime import datetime

from app.models.base import DonationProjectBaseModel


def investment_process(
    target: DonationProjectBaseModel,
    sources: list[DonationProjectBaseModel],
) -> list[DonationProjectBaseModel]:
    changed = []
    for source in sources:
        investment_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        changed.append(source)
        for changed_object in (source, target):
            changed_object.invested_amount += investment_amount
            if changed_object.full_amount == changed_object.invested_amount:
                changed_object.fully_invested = True
                changed_object.close_date = datetime.now()
        if target.fully_invested:
            break
    return changed
