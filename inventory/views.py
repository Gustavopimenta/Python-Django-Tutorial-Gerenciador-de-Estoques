from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory 
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, "inventory/inventory_list.html", context=context)

@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': Inventory
    }
    
    return render(request, "inventory/per_product.html", context=context)

@login_required
def add_product(request): 
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = float(add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
            new_inventory.save()
            return redirect("/inventory/")
    else:
        add_form = AddInventoryForm()
        
    return render(request, "inventory/inventory_add.html", {"form": add_form})
 
@login_required  
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    return redirect("/inventory/")

def update_inventory(request, pk):
    inventory = get_object_or_404(inventory, pk=pk)
    if request.method == "POST": 
        updateForm = UpdateInventoryForm()
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
            inventory.quantity_sold = updateForm.data['quantity_sold']
            inventory.cost_per_item = updateForm.data['cost_per_item']
            inventory.sales = float(inventory.cost_per_item) * float(inventory.quantity_sold)
            inventory.save()
            return redirect("/inventory/")
    else:
        updateForm = UpadateInventoryForm()
    context = {"form": updateForm}
    return render(request, "inventory/inventory_update.html", context=context)

 
