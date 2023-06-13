"""
Kudos - Vies
This file contains the views for the kudos blueprint.
"""

# Imports
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from src.kudos.forms import (
    KudoForm,
)
from flask_mail import Message
from src import db, mail
from src.models import (
    User,
    Departments,
    Kudo,
)


# Blueprint Configuration
kudos_bp = Blueprint("kudos", __name__)


# Kudos - Landing Page
@kudos_bp.route("/kudos")
@login_required
def kudos_landing_page():
    """
    Landing page for kudos
    """

    # Start Date for Dashboards (120 Days)
    start_date = datetime.now() - timedelta(days=120)

    # Dashboard - Count
    kudos_count = (
        db.session.query(
            db.func.count(Kudo.id).label("count"),
            db.func.strftime("%Y-%m", Kudo.created_date).label("month")
        )
        .filter(Kudo.created_date >= start_date)
        .group_by("month")
        .all()
    )
    kudos_graph_labels = [kudo.month for kudo in kudos_count]
    kudos_graph_data = [kudo.count for kudo in kudos_count]

    # Dashboard - Top 5 Receiving Users
    kudos_receiver = (
        db.session.query(
            User.firstname,
            User.lastname,
            db.func.count(Kudo.receiving_user_id).label("count")
        )
        .join(User, User.id == Kudo.receiving_user_id)
        .filter(Kudo.created_date >= start_date)
        .group_by(Kudo.receiving_user_id, User.firstname, User.lastname)
        .order_by(db.desc("count"))
        .limit(5)
        .all()
    )
    kudos_receiver_labels = [
        f"{kudo.firstname} {kudo.lastname}" for kudo in kudos_receiver
        ]
    kudos_receiver_data = [kudo.count for kudo in kudos_receiver]

    # Get the last 10 created kudos
    CreatingUser = db.aliased(User, name="CreatingUser")
    CreatingUserDepartment = db.aliased(
        Departments, name="CreatingUserDepartment")
    ReceivingUser = db.aliased(User, name="ReceivingUser")
    ReceivingUserDepartment = db.aliased(
        Departments, name="ReceivingUserDepartment")

    kudos = (
        db.session.query(
            Kudo.id,
            Kudo.submitting_user_id,
            Kudo.receiving_user_id,
            Kudo.kudo_message,
            Kudo.created_date,
            CreatingUser.firstname.label("creating_user_firstname"),
            CreatingUser.lastname.label("creating_user_lastname"),
            CreatingUser.department_id,
            CreatingUserDepartment.name.label("creating_user_department_name"),
            ReceivingUser.firstname.label("receiving_user_firstname"),
            ReceivingUser.lastname.label("receiving_user_lastname"),
            ReceivingUser.department_id,
            ReceivingUserDepartment.name.label(
                "receiving_user_department_name"),
        )
        .outerjoin(CreatingUser,
                   CreatingUser.id == Kudo.submitting_user_id)
        .outerjoin(CreatingUserDepartment,
                   CreatingUserDepartment.id == CreatingUser.department_id)
        .outerjoin(ReceivingUser,
                   ReceivingUser.id == Kudo.receiving_user_id)
        .outerjoin(ReceivingUserDepartment,
                   ReceivingUserDepartment.id == ReceivingUser.department_id)
        .order_by(Kudo.created_date.desc())
        .limit(10)
    )

    return render_template(
        "kudos/kudos.html",
        title="Kudos",
        kudos=kudos,
        kudos_graph_labels=kudos_graph_labels,
        kudos_graph_data=kudos_graph_data,
        kudos_receiver_labels=kudos_receiver_labels,
        kudos_receiver_data=kudos_receiver_data,
    )


# Kudos - Create Kudo
@kudos_bp.route("/kudos/create", methods=["GET", "POST"])
@login_required
def create_kudo():
    """
    Create a kudo
    """

    form = KudoForm()

    # User choices
    active_users = (
        db.session.query(
            User.id,
            User.firstname,
            User.lastname,
            User.status,
        )
        .filter(User.status == "active")
        .order_by(User.lastname.asc())
        .all()
    )

    form.receiving_user_id.choices = [
        (0, "Select a user")
    ] + [
        (user.id, user.firstname + " " + user.lastname)
        for user in active_users]

    # If user clicks cancel, redirect to kudos landing page
    if form.cancel.data:
        return redirect(url_for("kudos.kudos_landing_page"))

    # If form is submitted and valid, create kudo
    if form.validate_on_submit():

        # If user selects "0, Select a user", flash error message
        if form.receiving_user_id.data == 0:
            flash("Please select a user", "danger")
            return render_template("kudos/create_kudo.html",
                                   title="Create Kudo",
                                   form=form)

        # Create new kudo
        new_kudo = Kudo(
            submitting_user_id=current_user.id,
            receiving_user_id=form.receiving_user_id.data,
            kudo_message=form.kudo_message.data,
            created_date=datetime.utcnow(),
            created_by=current_user.id
        )

        db.session.add(new_kudo)
        db.session.commit()
        flash("Kudo created successfully!", "success")

        # Send email to receiving user
        receiving_user = (
            User.query.filter_by(id=form.receiving_user_id.data).first()
        )

        msg = Message(
            "KudoTrio - You have a new kudo!",
            recipients=[receiving_user.email],
            sender="noreply@healthtrio.com",
        )
        msg.body = f"""
Hello {receiving_user.firstname},

You have a new kudo from
{current_user.firstname} {current_user.lastname}.

Log in to view your kudos.
        """
        mail.send(msg)

        return redirect(url_for("kudos.kudos_landing_page"))

    return render_template("kudos/create_kudo.html",
                           title="Create Kudo",
                           form=form)
