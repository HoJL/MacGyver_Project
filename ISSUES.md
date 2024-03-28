# Issues
코드작성하면서 나온 주요 문제들
## 1. Pixmap 설정시 나오는 incorrect sRGB profile 경고
```
   libpng warning: iCCP: known incorrect sRGB profile
```
- #### 문제발생 이유와 해결방안
  - #### 문제발생 이유
    > png파일의 경우 흔히 sRGB프로파일을 사용하는데 이 프로파일이 예전 버전이거나 모종의이유로 유효하지 않을 수 있기때문에 png를 읽어올때 프로파일을 못읽어서 나오는 경고.

  - #### 해결방법
    > `imagemagick`을 설치해 `mogrify` 명령어를 사용하여 유효하지않은 프로파일을 삭제시켜줄 수 있다.  
    > 포토샵이 있으면 포토샵에서 웹용으로 저장을 하면 된다. 또는 프로필 할당에서 색상관리 안함을 눌러 설정해도 된다.

## 2. QWidget stylesheets가 적용이 안되는 현상
- #### 문제발생 이유와 해결방안
  - #### 문제발생 이유
    > Pyqt에서 QWidget을 사용한 파생 클래스에서는 기본설정으로 stylesheets를 무시하기 때문에 적용되지 않는다.

  - #### 해결방법
    > `setAttribute(WA_StyledBackground)`를 적용하면 된다. 기본설정으로 무시된 스타일을 사용하겠다는 설정이다.


## 3. QListWidget 사용시 insertItem 적용되지 않는 문제
QListWidget 사용시 insertItem 적용되지 않고 addItem과 똑같이 동작하는현상
- #### 문제발생 이유와 해결방안
  - #### 문제발생 이유
    > Qt공식문서에서 확인한결과 InsertItem을 사용하려면 Item을 처음 생성할때 부모위젯없이 생성하여야 한다고 되어있다.   
   그리고 InserItem이 되면 자동으로 해당Item의 부모가 된다고 나와있다.

   - #### 해결방법
     > 기존에 이렇게 사용했다면
     > ```
     > list_widget = QListWidget()
     > item = QListWidgetItem(list_widget)
     > list_widget.setItemWidget(item, OBJ)
     > list_widget.addItem(item) or list_widget.InsertItem(0, item)
     > ```

      > 이런식으로 바꾸어주면 된다.
      > ```
      > list_widget = QListWidget()
      > item = QListWidgetItem()
      > list_widget.InsertItem(0, item)
      > list_widget.setItemWidget(item, OBJ)
      > ```

## 4. 멀티쓰레드 사용시에 QTimer 동작하지않는 문제
```
 Timers cannot be started from another thread
 Timers cannot be stopped from another thread
```
- #### 문제발생 이유와 해결방안
  - #### 문제발생 이유
    > QTimer는 기본적으로 생성하여 실행하면 Main스레드의 event_loop에서 동작한다.   
    그래서 Main스레드가 아닌 다른 스레드에서 시작을 하기 위해서는 moveToThread를 사용하여 동작될 스레드에 넣어 주어야한다.   
    하지만 이 방법도 서로다른 스레드에서 시작과 중지를 할 수는 없다.

  - #### 해결방법
    > 시작 `signal`과 중지`signal`을 선언하고 동작을 연결시킨다음 실제로 시작과 중지를 하는곳에는 'signal'을 'emit'하기만 하면 된다.

    > >  `signal`로 동작이 되는 이유는 파이썬에서 `signal`은 항상 Main스레드에서만 동작하기 때문이다. 그래서 `signal`이 `emit`를 하여 함수를 실행시키면 함수는 Main스레드에서 실행되고 다시 해당 스레드로 돌아온다. 주의사항은 스레드에서 **Main스레드를 블락시키는 행동을 하면 동작을 하지 않는다는 점이다.** 그래서 `with` 이나 `thread.join` 과 같은 행동을 할때는 사용을 유의하여야한다. 
     
