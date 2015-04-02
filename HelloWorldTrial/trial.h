#ifndef TRIAL_H
#define TRIAL_H

#include <QMainWindow>

namespace Ui {
class Trial;
}

class Trial : public QMainWindow
{
    Q_OBJECT

public:
    explicit Trial(QWidget *parent = 0);
    ~Trial();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_actionLogin_triggered();

private:
    Ui::Trial *ui;
};

#endif // TRIAL_H
