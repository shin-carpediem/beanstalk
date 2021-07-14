from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum
import random
import string
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu
from .forms import ChooseTableForm


# Create your views here.
def non_login_user_random_code(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def index(request):
    return render(request, 'customer/index.html')


def table(request):
    user = request.user

    # print(request.session)
    # 新規/既存をセッションで判断する
    # 新規
    if not 'nonloginuser_uuid' in request.session:

        try:
            # TODO: be careful of id, client id should be 3.
            restaurant = User.objects.get(id=3)
        except Exception:
            # たかこうのアカウントID
            restaurant = User.objects.get(id=2)
        else:
            # 青木のアカウントID
            restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name

        if user.is_authenticated:
            return redirect('restaurant:logout')
        else:
            choose_table_form = ChooseTableForm(request.POST or None)

            ctx = {
                'choose_table_form': choose_table_form,
                'restaurant_name': restaurant_name,
            }

            return render(request, 'customer/table.html', ctx)
    # 既存
    else:
        messages.info(request, f'追加のオーダーの際は画面下の「戻る」ボタンを押してください')
        return redirect('customer:index')


def menu(request):
    user = request.user

    categories = Category.objects.defer('created_at').order_by('id')
    first_category = Category(id=0)
    menus = Menu.objects.defer('created_at').filter(
        category=first_category).order_by('-id')
    allergies = Allergy.objects.all().order_by('id')

    try:
        restaurant = User.objects.get(id=3)
    except Exception:
        restaurant = User.objects.get(id=2)
    else:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    if user.is_authenticated:
        table_num = '管理者'
    else:
        random_code = non_login_user_random_code(50)

        # TODO:
        # 新規の客かどうかをセッションで判断する
        # 新規
        if not 'nonloginuser_uuid' in request.session:

            try:
                table_num = request.POST.get('table')
            except:
                messages.info(request, f'申し訳ございません。再度「始める」を押してください')
                return redirect('customer:index')

            newuser = nonLoginUser(table=table_num,)
            newuser.save()
            uuid = str(newuser.uuid)

            # テーブル番号と客のuuidのセットになったセッションを作成
            request.session['nonloginuser_uuid'] = {1: uuid}
            # テーブル番号のセッションを作成
            request.session['table'] = {1: table_num}
            # テーブル番号と客のランダムコード(ワンタイムパスワード)のセットになったセッションを作成
            request.session['nonloginuser'] = {1: random_code}
        # 既存
        else:

            # print(request.session['table']['1'])
            try:
                table_num = request.session['table']['1']
            except:
                messages.info(request, f'申し訳ございません。再度「戻る」を押してください')
                return redirect('customer:index')

    if user.is_authenticated:
        ctx = {
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }
    else:
        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }

    return render(request, 'customer/menu.html', ctx)


@require_POST
def filter(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    category_name = request.POST.get('category')

    category_id = Category.objects.get(name=category_name)
    categories = Category.objects.defer('created_at').order_by('id')
    menus = Menu.objects.defer('created_at').filter(
        category=category_id).order_by('-id')
    allergies = Allergy.objects.defer('created_at').order_by('id')

    try:
        restaurant = User.objects.get(id=3)
    except Exception:
        restaurant = User.objects.get(id=2)
    else:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    # 店側から
    if user.is_authenticated:
        table_num = "管理者"
    # 客側から
    else:

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            # if random_code == request.session['nonloginuser'][table_num]:
            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

    ctx = {
        'random_code': random_code,
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'category_name': category_name,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }

    return render(request, 'customer/menu.html', ctx)


@require_POST
def menu_detail(request, menu_id):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.defer('created_at').order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    if user.is_authenticated:
        table_num = "管理者"
    else:

        try:

            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

    ctx = {
        'random_code': random_code,
        'menu': menu,
        'table_num': table_num,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_cart': "direct",
    }

    return render(request, 'customer/detail.html', ctx)


@require_POST
def cart(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    # uuid = request.session['nonloginuser_uuid'][table_num]
    uuid = request.session['nonloginuser_uuid']['1']

    if user.is_authenticated:
        table_num = "管理者"

    else:
        try:

            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
            else:
                None
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

    from .models import Cart

    # メニューの詳細から見るルート
    try:
        menu_id = request.POST.get('menu_id')

        menu_instance = Menu.objects.get(id=menu_id)
        cart_num = request.POST.get('cart_num')
        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        cart = Cart(menu=menu_instance, num=cart_num, customer=user_uuid)
        cart.save()
    # メニュー画面から見るルート
    except:
        None

    if request.POST.get('direct') == 'direct':

        try:
            restaurant = User.objects.get(id=3)
        except Exception:
            restaurant = User.objects.get(id=2)
        else:
            restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name

        categories = Category.objects.defer('created_at').order_by('id')
        first_category = Category(id=0)
        menus = Menu.objects.filter(category=first_category).order_by('-id')
        allergies = Allergy.objects.defer('created_at').order_by('id')

        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }

        return render(request, 'customer/menu.html', ctx)
    else:
        carts = Cart.objects.defer('created_at').filter(
            customer=uuid).order_by('-id')

        ctx = {
            'random_code': random_code,
            'table_num': table_num,
            'carts': carts,
        }

        return render(request, 'customer/cart.html', ctx)


@require_POST
def cart_detail(request, menu_id):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.defer('created_at').order_by('id')
    has_allergies = menu.allergies.defer('created_at').order_by('id')

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:

        try:

            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

        ctx = {
            'randcom_code': random_code,
            'table_num': table_num,
            'menu': menu,
            'allergies': allergies,
            'has_allergies': has_allergies,
        }

        return render(request, 'customer/detail.html', ctx)


@require_POST
def order(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    # uuid = request.session['nonloginuser_uuid'][table_num]
    uuid = request.session['nonloginuser_uuid']['1']

    categories = Category.objects.defer('created_at').order_by('id')
    first_category = Category(id=0)
    menus = Menu.objects.defer('created_at').filter(
        category=first_category).order_by('-id')

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:

        try:
            restaurant = User.objects.get(id=3)
        except Exception:
            restaurant = User.objects.get(id=2)
        else:
            restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name

        try:

            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

        try:
            from .models import Cart, Order
            users_cart = Cart.objects.defer('created_at').filter(
                customer=uuid).order_by('-id')
            user_uuid = nonLoginUser.objects.get(uuid=uuid)

            # cartからorderにコピー
            for each in users_cart:
                order = Order(status='調理中', menu=each.menu,
                              num=each.num, customer=user_uuid)
                order.save()

            # コピーし終わったcartは削除
            users_cart.delete()
        except:
            None

        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
        }

        messages.info(request, f"注文を承りました。今しばらくお待ちください")

        return render(request, 'customer/menu.html', ctx)


@require_POST
def history(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    uuid = request.session['nonloginuser_uuid']['1']

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:

        try:

            if random_code == request.session['nonloginuser']['1']:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {1: random_code}
        except:
            messages.info(request, f'申し訳ありませんがエラーが発生しました')
            return redirect('customer:index')

        from .models import Cart, Order
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
        carts = Cart.objects.defer('created_at').filter(
            customer=user_uuid).order_by('-id')
        orders = Order.objects.defer('created_at').filter(
            customer=user_uuid).order_by('-id')
        # _orders = Order.objects.filter(
        #     (Q(status='キャンセル') | Q(status='済')), customer=user)

        in_cart_each_price = 0
        in_order_each_price = 0

        # TODO:
        # for i in orders_in_cart:
        #     in_cart_each_price += 700 * int(orders_in_cart[i].num)

        # for i in orders_in_order:
        #     in_order_each_price += 700 * int(orders_in_order[i].num)

        # print(in_cart_each_price)
        # print(in_order_each_price)

        total_price = in_cart_each_price + in_order_each_price

        ctx = {
            'random_code': random_code,
            'table_num': table_num,
            'carts': carts,
            'orders': orders,
            'total_price': total_price,
        }

        return render(request, 'customer/history.html', ctx)
