from django import forms
from django.urls import reverse
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML, BaseInput
from .enums import UserGender
from .models import UserAddress

User = get_user_model()


def indicator_elm(id=None, use_gap=False):
    return f"""
        <div {f'id="{id}"' if id else ""} role="status" class="htmx-indicator">
            <svg aria-hidden="true" class="text-gray-200 size-5 {"me-3" if not use_gap else ""} animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span class="sr-only">Loading...</span>
        </div>
    """


def submit_btn(id, label="Cập nhật"):

    return f""" 
        <button 
            id="{id}"
            type="submit" 
            disabled
            class="disabled:bg-primary-400 disabled:cursor-not-allowed cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-4 py-1.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800" 
            > {label}
        </button>
    """


def delete_btn(
    id,
    delete_url,
    label="Xóa",
    confirm_msg="Xác nhận xóa?",
    indicator_id="indicator_delete",
    modal_close_id=None,
):
    return f"""
        <button 
            id="{id}"
            type="button" 
            hx-get="{delete_url}"
            hx-confirm="{confirm_msg}"
            hx-indicator="#{indicator_id}"
            hx-trigger="click"
            hx-disabled-elt="this"
            hx-swap="none"
            {f'modal-close-id="{modal_close_id}"' if modal_close_id else ""}
            class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-lg text-sm px-4 py-1.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" 
            > {label}
        </button>
    """


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     min_length=2,
    #     max_length=150,
    #     required=True,
    #     label="Tên",
    # )
    # last_name = forms.CharField(
    #     min_length=2,
    #     max_length=150,
    #     required=True,
    #     label="Họ",
    # )

    class Meta:
        model = User
        fields = (
            # "last_name",
            # "first_name",
            # "email",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.helper = FormHelper()
        # self.helper.form_method = "POST"
        # self.helper.form_action = "reverse('url_name')"

        self.helper.layout = Layout(
            # Div(
            #     Field("last_name", wrapper_class="mb-0"),
            #     Field("first_name", wrapper_class="mb-0"),
            #     css_class="flex flex-col md:flex-row gap-x-3 gap-y-4",
            # ),
            # Field("email"),
            Field("username"),
            Field("password1"),
            Field("password2"),
            Submit(
                "submit",
                "Đăng ký tài khoản",
                css_class="w-full cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
            ),
        )


class SignInForm(AuthenticationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            HTML(
                """
                <div class="flex items-start">
                    <div class="flex items-center h-5">
                        <input id="remember" aria-describedby="remember" name="remember" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800">
                    </div>
                    <div class="ml-3 text-sm">
                        <label for="remember" class="text-gray-500 select-none dark:text-gray-300">Lưu phiên đăng nhập</label>
                    </div>
                </div>
                """
            ),
            Submit(
                "submit",
                "Đăng nhập",
                css_class="w-full cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
            ),
        )


class UpdateUserInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label="Giới tính",
        required=False,
        widget=forms.widgets.RadioSelect,
        choices=UserGender.choices,
    )
    birthday = forms.DateField(
        label="Ngày sinh",
        input_formats=["%d-%m-%Y"],
        required=False,
        widget=forms.DateInput(),
    )
    bio = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    class Meta:
        model = User
        fields = ["last_name", "first_name", "gender", "birthday", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "w-full space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('update_info_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_info_submit",
            "hx-post": reverse("htmx_update_info"),
        }

        self.helper.layout = Layout(
            Div(
                Field("last_name", wrapper_class="w-full !mb-0"),
                Field("first_name", wrapper_class="w-full !mb-0"),
                css_class="flex flex-col md:flex-row gap-x-3 gap-y-4",
            ),
            Field("gender", template="crispy_form/inline_radio_group.html"),
            Field("birthday", template="crispy_form/datepicker.html"),
            Field("bio"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("update_info_submit")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateUserContact(forms.ModelForm):
    phone = forms.CharField(
        min_length=10,
        max_length=10,
        label="Số điện thoại",
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('update_contact_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_contact_submit",
            "hx-on::after-request": "closeModal('update-contact-modal');",
            "hx-post": reverse("htmx_update_contact"),
        }

        self.helper.layout = Layout(
            Field("email"),
            Field("phone"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("update_contact_submit")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateUserAddress(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ["address"]

    def __init__(self, *args, **kwargs):
        address_instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

        delete_url = ""
        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.form_show_labels = True
        self.helper.attrs = {
            "oninput": "enableButton('update_address_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_address_submit",
        }

        if address_instance:
            delete_url = reverse(
                "htmx_delete_address",
                args=[address_instance.id],
            )
            self.helper.attrs["hx-post"] = reverse(
                "htmx_update_address",
                args=[address_instance.id],
            )

        self.helper.layout = Layout(
            Field("address", wrapper_class="!mb-0 w-full"),
            Div(
                HTML(indicator_elm("indicator_delete", True)),
                HTML(
                    delete_btn(
                        "delete_address_btn",
                        delete_url,
                        confirm_msg="Bạn có chắc chắn muốn xóa địa chỉ này?",
                        modal_close_id="update-address-modal",
                    )
                ),
                HTML(submit_btn("update_address_submit")),
                css_class="flex items-center justify-end gap-3",
            ),
        )


class AddUserAddress(UpdateUserAddress):
    address = forms.CharField(
        min_length=20,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Thêm địa chỉ mới"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_class = "flex items-center gap-4"
        self.helper.form_show_labels = False
        self.helper.attrs = {
            "oninput": "enableButton('add_address_submit');",
            "hx-target": "#update-address-div",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #add_address_submit",
            "hx-post": reverse("htmx_add_address"),
        }

        self.helper.layout = Layout(
            Field("address", wrapper_class="!mb-0 w-full"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("add_address_submit", "Thêm")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateUserAvatar(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]


class ChangePasswordFormCustom(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = ""
        self.fields["new_password2"].help_text = ""
        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('change_password_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #change_password_submit",
            "hx-post": reverse("htmx_change_password"),
        }

        self.helper.layout = Layout(
            Field("old_password"),
            Field("new_password1"),
            Field("new_password2"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("change_password_submit")),
                css_class="flex items-center justify-end",
            ),
        )
