# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from views.LoginView import LoginView
from views.SignUpView import SignUpView
from views.MainMenuView import MainMenuView
from views.InputTextView import InputTextView
from views.ResultView import ResultView
from logics.DataController import DataController
from views.SaveResultView import SaveResultView
from views.UploadView import UploadView

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TXT Scan")
        self.resize(800, 600)
        self.center()
        self.currentUser = None
        self.dataController = None
        self.lastResult = None
        self.showLoginView()

    # 로그인 화면
    def showLoginView(self):
        loginView = LoginView(goSignup=self.showSignUpView, goMainMenu=self.showMainMenuView)
        self.setCentralWidget(loginView)

    # 회원가입 화면
    def showSignUpView(self):
        signUpView = SignUpView(signUpCallBack=self.showLoginView)
        self.setCentralWidget(signUpView)

    # 메인메뉴
    def showMainMenuView(self):
        if  not self.dataController:
            self.currentUser = "user"
            self.dataController = DataController(self.currentUser)

        menuView = MainMenuView(
            goInputText=self.showInputTextView,
            goUpload=self.showUploadView,
            goResult=self.showResultView,
            goSave=self.showSaveResultView,
            logout=self.showLoginView
        )
        self.setCentralWidget(menuView)

    # 화면을 중앙에 배치하게 만듦
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    # 텍스트 입력 화면
    def showInputTextView(self):
        inputView = InputTextView(dataController=self.dataController, goResult=self.showResultView, goBack=self.showMainMenuView)
        self.setCentralWidget(inputView)

    # 결과 화면
    def showResultView(self, result=None):
        if result is not None and isinstance(result, str):
            self.lastResult = result  # 새로 들어온 결과를 저장
        elif self.lastResult is None:
            self.lastResult = "[결과가 없습니다.]"

        resultView = ResultView(self.lastResult, goBack=self.showMainMenuView, dataController=self.dataController)
        self.setCentralWidget(resultView)

    # 결과 리스트 화면
    def showSaveResultView(self):
        view = SaveResultView(self.currentUser, goBack=self.showMainMenuView)
        self.setCentralWidget(view)

    # 업로드 화면
    def showUploadView(self):
        uploadView = UploadView(dataController=self.dataController, goResult=self.showResultView, goBack=self.showMainMenuView)
        self.setCentralWidget(uploadView)

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()