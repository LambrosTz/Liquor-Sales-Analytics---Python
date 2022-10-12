import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("liquor_sales_2016_2019.csv")
#print(data.columns)
#%%
data=data.drop(['invoice_and_item_number', 'date',
       'address', 'city', 'store_location', 'county_number',
       'county', 'category', 'category_name', 'vendor_number', 'vendor_name',
       'pack', 'bottle_volume_ml','state_bottle_cost', 'state_bottle_retail',
       'sale_dollars', 'volume_sold_liters', 'volume_sold_gallons','item_number'],axis=1)
#%%
data['zip_code']=data['zip_code'].apply(lambda x: int(x))

#%%                          Most Popular Item
#print(data.columns)

data1=data.drop(['store_number', 'store_name'],axis=1).groupby(['zip_code','item_description'],as_index=False)
#%%
pop_item=data1.agg(np.sum).sort_values(['zip_code','bottles_sold'],ascending=[True,False])
#%%
#print(pop_item)
#print(len(data['zip_code'].unique()))
#print(len(data['item_description'].unique()))
#%%
pop_item=pop_item.groupby('zip_code',as_index=False).max()

#%%
pop_item=pop_item.sort_values('zip_code')
print(pop_item)
pop_item.to_csv('Most Popular Item per Zip Code.csv',index=False)

#%%
#print(pop_item.bottles_sold.max())
plt.figure(figsize=(16,9))
for item in pop_item['item_description'].unique():
    plt.scatter('zip_code', 'bottles_sold',data=pop_item[pop_item.item_description==item],
                s=30*np.log(pop_item[pop_item.item_description==item].bottles_sold))
plt.legend(labels=pop_item['item_description'].unique(),loc=(1.02,0.01))
plt.title('Most Popular Item per Zipcode')
plt.xlabel('Zip Code')
plt.ylabel('Bottles Sold')
#plt.yscale('log')

plt.grid()

plt.tight_layout()
plt.savefig('Most Popular Item per Zip Code.png',dpi=600)
plt.show()


#%%                     Percentage of Sales per Store
#print(data.columns)
data2=data.drop(['store_number','zip_code','item_description'],axis=1)
data2=data2.groupby('store_name').sum()
total=data2.sum().values[0]
data2.columns=['Sales Percentage']
data2['Sales Percentage']=np.round(100*data2['Sales Percentage']/total,2)
print(data2)
data2.to_csv('Percentage of Sales per Store.csv')
#%%
plt.figure(figsize=(16,12))
plt.barh(data2.index,data2['Sales Percentage'])

plt.title('Percentage of Sales per Store')
plt.xlabel('Sales Percentage ( % )')
plt.ylabel('Store')
#plt.yscale('log')

plt.grid()

plt.tight_layout()
plt.savefig('Percentage of Sales per Store.png',dpi=600)
plt.show()
