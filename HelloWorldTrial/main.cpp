#include "trial.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Trial w;
    w.show();

    return a.exec();
}
