# NutriMate

**NutriMate**는 사용자의 신체 정보와 식사 내용을 기반으로  
하루 섭취해야 할 열량 및 영양소를 계산하고,  
저녁 메뉴를 선형계획법(Linear Programming)을 통해 **맞춤 추천**해주는 식단 관리 GUI 프로그램입니다.

> 이 프로젝트는 팀 프로젝트로 진행되었으며, 본 저장소는 개인 포트폴리오용으로 정리한 것입니다.

---

## 기여 내용
- **역할**: 
  - 식약처 제공 식품 데이터셋의 전처리 및 구조 정리 (Pandas, Numpy 활용)
  - `scipy.optimize.linprog()` 기반 **최적화 알고리즘 구현**

---

## 주요 기능

- 키, 몸무게, 나이, 성별을 통한 BMR/TDEE 계산
- 다이어트, 벌크업, 케토 중 목적에 맞춘 섭취량 비율 설정
- 아침/점심 식단 입력 후 남은 영양소 계산
- Scipy의 `linprog()`를 활용한 최적화 기반 저녁 식단 추천

---

## 기술 스택

- **Python 3.x**
- **Tkinter** - 데스크탑 GUI
- **Pandas / NumPy** - 데이터 처리
- **SciPy.optimize** - 선형계획법을 활용한 최적화

---

## AI 기반

NutriMate는 머신러닝 기반 학습은 포함하지 않지만,  
**지능적인 최적 의사결정(Linear Programming)**을 활용하여  
남은 영양소 섭취량에 대한 **수학적 최적 해**를 도출합니다.

---

## 실행 방법
```bash
pip install pandas numpy scipy
python NutriMate.py
```
> NutriMate.py와 food.xlsx 파일은 같은 디렉토리에 있어야 합니다.
