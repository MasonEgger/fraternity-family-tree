from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import RequestContext
from fraternity_tree.models import Brother, PledgeClass

from .forms import FamilyTreeForm, PledgeClassForm


def index(request):
    # Brother.objects.rebuild()
    return render(
        request,
        "fraternity_tree/tree.html",
        {
            "brothers": Brother.objects.all(),
        },
    )


def my_tree(request):
    brother_list = []
    tmp_list = Brother.objects.all().order_by(
        "last_name", "first_name", "pledge_class__date_initiated"
    )
    for brother in tmp_list:
        brother_list.append((brother.id, brother.__str__()))
    if request.method == "POST":
        form = FamilyTreeForm(request.POST, data_list=brother_list)
        if form.is_valid():
            try:
                brother_id = form.cleaned_data["name"]
                generations = form.cleaned_data["generations"]
                if generations is None:
                    generations = 0
                brother = Brother.objects.get(pk=brother_id)
                if generations > 0:
                    brother = brother.get_ancestors()
                    if generations >= len(brother):
                        brother = brother[0]
                    else:
                        brother = brother[len(brother) - generations]

                return render(
                    request,
                    "fraternity_tree/tree.html",
                    {"brothers": brother.get_descendants(include_self=True)},
                )
            except Exception as e:
                return HttpResponse(
                    "Exception %s was thrown. Report this error to the site adminstrator"
                    % e
                )
    else:
        form = FamilyTreeForm(data_list=brother_list)
    return render(
        request,
        "fraternity_tree/my_tree.html",
        {
            "form": form,
        },
    )


def pledge_class(request):
    pledge_classes = []
    pc = PledgeClass.objects.all().order_by("date_initiated")
    for pclass in pc:
        pledge_classes.append((pclass.get_name(), pclass.get_name()))
    if request.method == "POST":
        form = PledgeClassForm(request.POST, data_list=pledge_classes)
        if form.is_valid():
            # try:
            pledge_class = form.cleaned_data["pledge_class"]
            print(pledge_class)
            pledge_class = PledgeClass.objects.get(name=pledge_class)
            pledge_brothers = (
                Brother.objects.all()
                .filter(pledge_class=pledge_class)
                .order_by("last_name", "first_name")
            )
            return render(
                request,
                "fraternity_tree/pledge_class.html",
                {
                    "pledge_brothers": pledge_brothers,
                },
            )
            # except Exception as e:
            #    return HttpResponse("Exception %s was thrown. Report this error to the site adminstrator" % e)
    else:
        form = PledgeClassForm(data_list=pledge_classes)
    return render(
        request,
        "fraternity_tree/my_pledge_class.html",
        {
            "form": form,
        },
    )
