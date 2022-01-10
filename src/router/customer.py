from datetime import datetime

from fastapi import APIRouter, Request, status
from pony.orm import db_session
from fastapi import Depends
from ..config.auth import get_current_user
from ..models.schemasIn import CustomerIn, UserIn
from ..models.schemasOut import CustomerOut
from ..models.model import Model
from ..utils import customerUtil
from datetime import date
from typing import Optional
from ..utils import imageConvert

router = APIRouter()


@router.post('/customer', tags=['Customers'])
def create_customer(request: CustomerIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        try:
            check, validation = customerUtil.validation(request)
            if not check:
                return validation

            profile_img = ''
            if request.profile_img:
                profile_img = imageConvert.base64_pil(request.profile_img)
            customer = Model.Customer(
                cus_code=customerUtil.getCusCode(),
                first_name=request.first_name if request.first_name is not None else "",
                last_name=request.last_name if request.last_name is not None else "",
                gender=request.gender if request.gender is not None else "",
                dob=request.dob if request is not None else "",
                phone=request.phone if request.dob is not None else "",
                nationality=request.nationality if request.nationality is not None else "",
                email=request.email if request.email is not None else "",
                identity_type=request.identity_type if request.identity_type is not None else "",
                identity_number=request.identity_number if request.identity_number is not None else "",
                identity_date=request.identity_date if request.identity_date is not None else "",
                id_card=request.id_card if request.id_card is not None else "",
                house_no=request.house_no if request.house_no else "",
                street_no=request.street_no if request.street_no is not None else "",
                address=request.address if request.address is not None else "",
                status="Inactive",
                profile_img=profile_img,
                attachment_file=request.attachment_file if request.attachment_file is not None else "",
                occupation=request.occupation if request.occupation is not None else "",
                income=request.income if request.income is not None else 0,
                issue_date=request.issue_date if request.issue_date else None,
                issue_expired=request.issue_expired if request.issue_expired else None,
                expense=request.expense if request.expense else 0,
                updated_by=request.updated_by if request.updated_by is not None else 0,
                created_by=request.created_by if request.created_by is not None else 0,
                created_at=request.created_at if request.created_at is not None else date.today(),
                updated_at=request.created_at if request.created_at is not None else date.today(),
            )
        except RuntimeError:
            pass

        return {
            'success': 1,
            'data': CustomerIn.from_orm(customer)
        }


@router.get('/customer', tags=['Customers'])
def get_all_customer(name: Optional[str] = None, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        if name:
            customer = Model.Customer.select(lambda cu: getName(name) in (cu.first_name + " " + cu.last_name).lower())
        else:
            customer = Model.Customer.select()
        if not customer:
            return {
                'success': 0,
                'message': 'Customer is empty!'
            }
        return {
            'success': 1,
            'data': [customerResource(c) for c in customer]
        }


def customerResource(customer: Model.Customer):
    with db_session:
        active = 0
        disbursements = Model.Disbursement.select(lambda d: d.cus_id==customer.id)
        if disbursements:
            active=1
        return {
            "id":customer.id,
            "cus_code": customer.cus_code,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "gender": customer.gender,
            "dob": customer.dob,
            "phone": customer.phone,
            "nationality": customer.nationality,
            "email": customer.email,
            "identity_type": customer.identity_type,
            "identity_number": customer.identity_number,
            "identity_date": customer.identity_date,
            "id_card": customer.id_card,
            "house_no": customer.house_no,
            "street_no": customer.street_no,
            "address": customer.address,
            "status": customer.status,
            "profile_img": customer.profile_img,
            # "attachment_file": customer.attachment_file,
            "occupation": customer.occupation,
            "income": customer.income,
            "issue_date": customer.issue_date,
            "issue_expired": customer.issue_expired,
            "expense": customer.expense,
            "updated_by": customer.updated_by,
            "created_by": customer.created_by,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            # "deleted_at": c,
            "active": active
        }

@router.get('/customer/{id}', tags=['Customers'])
def get_customer_by_id(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.get(lambda c: c.id == id)
        if not customer:
            return {
                'success': 0,
                'message': f'Customer Id:{id} not found'
            }
        return CustomerOut.from_orm(customer)


@router.put('/customer/{id}', tags=['Customers'])
def update_customer(id: int, request: CustomerIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.get(lambda c: c.id == id)
        if not customer:
            return {
                'success': 0,
                'message': f'Customer Id:{id} not found'
            }

        # check, validation = customerUtil.validation(request)
        # if not check:
        #     return validation

        profile_img = customer.profile_img
        if request.profile_img:
            profile_img = imageConvert.base64_pil(request.profile_img)
        try:
            customer.first_name = request.first_name if request.first_name is not None else customer.first_name
            customer.last_name = request.last_name if request.last_name is not None else customer.last_name
            customer.gender = request.gender if request.gender is not None else customer.gender
            customer.dob = request.dob if request is not None else customer.dob
            customer.phone = request.phone if request.dob is not None else customer.phone
            customer.nationality = request.nationality if request.nationality is not None else customer.nationality
            customer.email = request.email if request.email is not None else customer.email
            customer.identity_type = request.identity_type if request.identity_type is not None else customer.identity_type
            customer.identity_number = request.identity_number if request.identity_number is not None else customer.identity_number
            customer.identity_date = request.identity_date if request.identity_date is not None else customer.identity_date
            customer.id_card = request.id_card if request.id_card is not None else customer.id_card
            customer.house_no = request.house_no if request.house_no else customer.house_no
            customer.street_no = request.street_no if request.street_no is not None else customer.street_no
            customer.address = request.address if request.address is not None else customer.address
            customer.status = request.status if request.status is not None else customer.status
            customer.profile_img = profile_img
            customer.attachment_file = request.attachment_file if request.attachment_file is not None else customer.attachment_file
            customer.occupation = request.occupation if request.occupation is not None else customer.occupation
            customer.income = request.income if request.income is not None else customer.income
            customer.issue_date = request.issue_date if request.issue_date else customer.issue_date
            customer.issue_expired = request.issue_expired if request.issue_expired else customer.issue_expired
            customer.expense = request.expense if request.expense else customer.expense
            customer.updated_by = request.updated_by if request.updated_by is not None else customer.updated_by
            customer.updated_at = request.updated_at if request.updated_at is not None else date.today()
        except ValueError:
            pass
        return {
            'success': 1,
            'message': 'Update is successful'
        }


@router.delete('/customer/{id}', tags=['Customers'])
def delete_customer(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.select(lambda c: c.id == id)
        if customer:
            cus_id = [c.id for c in customer]
            disbursement = Model.Disbursement.select(lambda d: d.cus_id in cus_id and d.status == 'Approved')
            if disbursement:
                return {
                    'success': 0,
                    'message': 'Customer is active'
                }
            customer.delete()
            return {
                'success': 1,
                'message': 'Delete successfully'
            }
        return {
            'success': 0,
            'message': f'Customer Id:{id} not found'
        }


def getName(name):
    name = name.lower()
    # name = name.replace(" ", '')
    return name
