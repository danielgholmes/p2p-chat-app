#include "trial.h"
#include "ui_trial.h"
#include <QInputDialog>

Trial::Trial(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Trial)
{
    ui->setupUi(this);
}

Trial::~Trial()
{
    delete ui;
}

void Trial::on_pushButton_clicked()
{
    ui->textEdit->setText("Hi there :) ");
}

void Trial::on_pushButton_2_clicked()
{
    ui->textEdit->clear();
}

void Trial::on_pushButton_3_clicked()
{
    ui->textEdit->append("You've joined this chat");
}

void Trial::on_pushButton_4_clicked()
{
    ui->textEdit_2->setText("Refreshed");
}

void Trial::on_actionLogin_triggered()
{
    bool ok;

    QString text = QInputDialog::getText(this,
                "Please enter your user credentials", "Username:", QLineEdit::Normal,QString::null, &ok);

    if(ok && !text.isEmpty()){
        ui->textEdit_3->append(text);
    } else {
        ui->textEdit_3->append("Failed...");
    }
}
