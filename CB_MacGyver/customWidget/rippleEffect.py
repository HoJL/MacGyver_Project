from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from attr import dataclass

@dataclass
class Ripple:
    '''Ripple효과를 사용하기 위한 구조체
    '''
    ripple: QWidget = None
    aniGroup: QParallelAnimationGroup = None

class IconButton(QToolButton):

    def __init__(self, parent, maxSize = 30) -> None:
        super().__init__(parent)
        self.rippleList = list([Ripple])
        self.rippleList.clear()
        self._duration = 500
        self._maxSize = maxSize

    # def mousePressEvent(self, event: QMouseEvent | None) -> None:
    #     super().mousePressEvent(event)
    #     if event.buttons() & Qt.MouseButton.LeftButton:
    #         self.drawRipple(event.x(), event.y())
    #         #print('%d  %d'%(event.x(), event.y()))

    def drawRipple(self, x, y):
        '''클릭 애니매이션 생성해서 그리기
        x: x좌표
        y: y좌표\n
        좌표 중앙을 중심으로 그려진다
        '''
        temp = Ripple()
        rip = QWidget(self)
        rip.setStyleSheet("background-color: rgba(100, 100, 100, 0.6); border-radius: 0;")
        rip.show()
        
        ani = QPropertyAnimation(rip, b'geometry')
        startRect = QRect(0, 0, 0, 0)
        startRect.moveCenter(QPoint(x, y))
        ani.setStartValue(startRect)
        endRect = QRect(0, 0, self._maxSize, self._maxSize)
        endRect.moveCenter(QPoint(x, y))
        ani.setEndValue(endRect)
        ani.setDuration(self._duration)
        ani.setEasingCurve(QEasingCurve.InOutCubic)

        ani2 = QVariantAnimation(rip)
        ani2.setStartValue(0)
        ani2.setEndValue(self._maxSize)
        ani2.setDuration(self._duration)
        ani2.valueChanged.connect(lambda: self._rippleChanged(ani2.currentValue(), rip))

        aniGroup = QParallelAnimationGroup()
        aniGroup.addAnimation(ani)
        aniGroup.addAnimation(ani2)

        temp.ripple = rip
        temp.aniGroup = aniGroup
        
        self.rippleList.append(temp)
        ani.finished.connect(self._rippleFinished)
        aniGroup.start()
        
    def _rippleFinished(self):
        ''' 애니매이션이 끝났을때 실행되는 함수\n
        다끝난 애니메이션을 지운다
        '''
        self.rippleList[0].ripple.resize(0, 0)
        self.rippleList[0].ripple.deleteLater()
        self.rippleList[0].aniGroup.deleteLater()
        del self.rippleList[0]

    def _rippleChanged(self, value, rip):
        '''애니메이션 진행시에 위젯을 원으로 만들어주는 함수
        value: 애니메이션 현재Value
        rip: 원으로만들 위젯
        '''
        rip.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); border-radius: %fpx;"% (value/2.1))