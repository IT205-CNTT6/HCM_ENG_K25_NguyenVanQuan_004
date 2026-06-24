def get_validate (prompt:str,input_type:str ="str",empty_allow :bool = False):
    while True:
        user_input = input(prompt)
        if not user_input:
            print("Không được để trống !")
            continue
        if input_type == "float":
            value = float(user_input)
            if value <= 0:
                print("Phải là số dương khác không !")
                continue
            return value
        if input_type =="int":
            value = int(user_input)
            if value <= 0 :
                print("Phải là số nguyên dương khác không !")
                continue
            return value
        return user_input

def menu():
    print("""
===================Menu=====================
1. Hiển thị danh sách đơn hàng
2. Thêm đơn hàng mới 
3.Cập nhật đơn hàng
4. Xóa đơn hàng
5. Tìm kiếm đơn hàng
6. thoát
============================================
""")

class Order:
    def __init__(self,id_order,customer_name,product_name,unit_price,quantity,shipping_fee,voucher):
        self.id = id_order 
        self.customer_name = customer_name
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity
        self.shipping_fee = shipping_fee
        self.voucher = voucher
        self.total_mount = 0
        self.order_type = ""

        self.calculate_total_amount()
        self.classify_order()


    def calculate_total_amount(self):
        self.total_mount = self.unit_price * self.quantity  + self.shipping_fee - self.voucher
        return self.total_mount

    def classify_order(self):
        if self.total_mount < 500000:
            self.order_type ="Nhỏ"
        elif 500000 <= self.total_mount < 2000000:
            self.order_type ="Trung bình"
        elif 2000000 <= self.total_mount < 10000000:
            self.order_type ="Lớn"
        else:
            self.order_type ="VIP"

class OrderManager:
    def __init__(self):
        self.orders: list[Order] = []

    def show_all (self,data_list = None):
        show_order = data_list if data_list is not None else self.orders
        try:
            if not show_order:
                raise ValueError("Danh sách rỗng !")
            print("Danh sách đơn hàng")
            print(f"{"Mã đơn hàng":<10} | {"Tên khách hàng":<15} | {"Tên sản phẩm":<15} | {"Đơn giá":<15} | {"Số lượng":<10} | {"Phí vận chuyển":<15} | {"Voucher":<15} | {"Tổng tiền":<15} | {"Phân loại đơn hàng":<10}")
            for ord in show_order:
                print(f"{ord.id:<10} | {ord.customer_name:<15} | {ord.product_name:<15} | {ord.unit_price:<15} | {ord.quantity:<10} | {ord.shipping_fee:<15} | {ord.voucher:<15} | {ord.total_mount} | {ord.order_type}")

        except ValueError as e:
            print(f"Lỗi: {e}")
    
    def found_id (self,id_order: str):
        for ord in self.orders:
            if(id_order.lower() == ord.id.lower()):
                return ord
            return None


    def add_order(self):
        while True:
            id_order = get_validate("Nhập mã đơn hàng: ")
            if self.found_id(id_order) is not None:
                print("ID đơn hàng bị trùng !")
                continue
            else:
                customer_name = get_validate("Nhập tên khách hàng: ")
                product_name = get_validate("Nhập tên đơn hàng: ")
                unit_price =get_validate("Nhập đơn giá sản phẩm ","float")
                quantity = get_validate("Nhập số lượng mua: ","float")
                shipping_fee = get_validate("Nhập phí vận chuyển: ","float")
                voucher = get_validate("Nhập số tiền giảm giá: ")
                new_ord = Order(id_order,customer_name,product_name,unit_price,quantity,shipping_fee,voucher)
                self.orders.append(new_ord)
                print("Thêm đơn hàng thành công !")
                break
    
    def update_order(self):
        id_order = get_validate("Nhập id cần cập nhật: ")
        target_ord = self.found_id(id_order)
        if target_ord is None:
            print("ID không tồn tại trong danh sách !")

        target_ord.id = get_validate("Nhập đơn giá mới: ","float")
        target_ord.quantity = get_validate("Nhập số lượng mới: ","int")
        target_ord.shipping_fee= get_validate("Nhập phí vận chuyển mới: ","float") 
        target_ord.voucher = get_validate("Nhập voucher mới: ","float")
        target_ord.calculate_total_amount()
        target_ord.classify_order()
        print("Đã cập nhật thành công !")

    def delete_order(self):
        id_order = get_validate("Nhập id cần xóa: ")
        target_ord = self.found_id(id_order)
        if target_ord is None:
            print("ID không tồn tại trong danh sách !")
        while True:
            select = input("Bạn có chắc muốn xía đơn hàng này không ?(Y/N): ").lower()
            match select:
                case 'y':
                    self.orders.remove(target_ord)
                    print("Xóa đơn hàng thành công !")
                    return
                case 'n':
                    print("Hủy xóa đơn hàng")
                    return
                case _ :
                    print("Bạn nhập sai !")

    def search_order(self):
        customer_order = get_validate("Nhập tên khách hàng cần tìm: ")
        list_order = []
        for ord in self.orders:
            if(customer_order.lower() in ord.customer_name.lower()):
                list_order.append(ord)
        if list_order:
            self.show_all(list_order)
        else:
            print("Không tìm thấy tên khách hàng")

def main():
    orderManager = OrderManager()
    orderManager.orders = [
        Order("101","Nguyễn Văn A","bàn phím",20000000,2,10000,200000)
    ]
    while True:
        menu()
        choice = input("Nhập lựa chọn của bạn: ")
        match choice:
            case '1':
                orderManager.show_all()
            case '2':
                orderManager.add_order()
            case '3':
                orderManager.add_order()
            case '4':
                orderManager.delete_order()
            case '5':
                orderManager.search_order()
            case '6':
                print("Đã thoát khỏi chương trình !")
                break


main()