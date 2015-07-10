# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 15:38:57 2014

@author: thomasaref
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item#, Group
from chaco.api import PlotAxis, GridDataSource, GridMapper, DataRange2D, CMapImagePlot, \
    VPlotContainer, ImageData, DataRange1D, LinearMapper, ColorBar, Plot, ArrayPlotData, jet,\
    HPlotContainer
from enable.component_editor import ComponentEditor
from numpy import squeeze, transpose
from chaco.tools.api import PanTool, ZoomTool, LineInspector
import h5py
from numpy import amin, amax

        
class myImagePlot(HasTraits):
    # container for all plots
    container = Instance(HPlotContainer)
    
    # Plot components within this container:
    color_plot = Instance(CMapImagePlot)
    vertical_cross_plot = Instance(Plot)
    horizontal_cross_plot = Instance(Plot)
    colorbar = Instance(ColorBar)
    
    # plot data
    pd_all = Instance(ArrayPlotData)
    pd_horiz=Instance(ArrayPlotData)
    pd_vert=Instance(ArrayPlotData)
    #private data storage
    _imag_index=Instance(GridDataSource)
    _image_value=Instance(ImageData)   
    
    traits_view = View(
        Item('container', editor=ComponentEditor(), show_label=False),
        width=1000, height=700, resizable=True, title="Chaco Plot")

    def __init__(self, x,y,z):
        super(myImagePlot, self).__init__()
        self.pd_all = ArrayPlotData(imagedata = z)
        self.pd_horiz = ArrayPlotData(x=x, horiz=z[4, :])
        self.pd_vert = ArrayPlotData(y=y, vert=z[:,5])
    
        self._imag_index = GridDataSource(xdata=x, ydata=y, sort_order=("ascending","ascending"))
        index_mapper = GridMapper(range=DataRange2D(self._imag_index))
        self._imag_index.on_trait_change(self._metadata_changed,
                                          "metadata_changed")
        self._image_value = ImageData(data=z, value_depth=1)
        color_mapper = jet(DataRange1D(self._image_value))

        self.color_plot= CMapImagePlot(
            index=self._imag_index,
            index_mapper=index_mapper,
            value=self._image_value,
            value_mapper=color_mapper,
            padding=20,
            use_backbuffer=True,
            unified_draw=True)

        #Add axes to image plot            
        left = PlotAxis(orientation='left',
                        title= "Frequency (GHz)",
                        mapper=self.color_plot.index_mapper._ymapper,
                        component=self.color_plot)

        self.color_plot.overlays.append(left)
        
        bottom = PlotAxis(orientation='bottom',
                        title= "Time (us)",
                        mapper=self.color_plot.index_mapper._xmapper,
                        component=self.color_plot)
        self.color_plot.overlays.append(bottom)

        self.color_plot.tools.append(PanTool(self.color_plot,
                                           constrain_key="shift"))
        self.color_plot.overlays.append(ZoomTool(component=self.color_plot,
                                            tool_mode="box", always_on=False))
                                            
        #Add line inspector tool for horizontal and vertical
        self.color_plot.overlays.append(LineInspector(component=self.color_plot,
                                               axis='index_x',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               is_listener=True,
                                               color="white"))

        self.color_plot.overlays.append(LineInspector(component=self.color_plot,
                                               axis='index_y',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               color="white",
                                               is_listener=True))         

        myrange = DataRange1D(low=amin(z),
                              high=amax(z))
        cmap=jet                         
        self.colormap = cmap(myrange)

        # Create a colorbar
        cbar_index_mapper = LinearMapper(range=myrange)
        self.colorbar = ColorBar(index_mapper=cbar_index_mapper,
                                 plot=self.color_plot,
                                 padding_top=self.color_plot.padding_top,
                                 padding_bottom=self.color_plot.padding_bottom,
                                 padding_right=40,
                                 resizable='v',
                                 width=30)#, ytitle="Magvec (mV)")

        #create horizontal line plot
        self.horiz_cross_plot = Plot(self.pd_horiz, resizable="h")
        self.horiz_cross_plot.height = 100
        self.horiz_cross_plot.padding = 20
        self.horiz_cross_plot.plot(("x", "horiz"))#,
                             #line_style="dot")
#        self.cross_plot.plot(("scatter_index","scatter_value","scatter_color"),
#                             type="cmap_scatter",
#                             name="dot",
#                             color_mapper=self._cmap(image_value_range),
#                             marker="circle",
#                             marker_size=8)

        self.horiz_cross_plot.index_range = self.color_plot.index_range.x_range

        #create vertical line plot
        self.vert_cross_plot = Plot(self.pd_vert, width = 140, orientation="v", 
                                resizable="v", padding=20, padding_bottom=160)
        self.vert_cross_plot.plot(("y", "vert"))#,
#                             line_style="dot")
       # self.vert_cross_plot.xtitle="Magvec (mV)"
 #       self.vertica_cross_plot.plot(("vertical_scatter_index",
 #                              "vertical_scatter_value",
 #                              "vertical_scatter_color"),
 #                            type="cmap_scatter",
 #                            name="dot",
 #                            color_mapper=self._cmap(image_value_range),
 #                            marker="circle",
  #                           marker_size=8)

        self.vert_cross_plot.index_range = self.color_plot.index_range.y_range

        # Create a container and add components
        self.container = HPlotContainer(padding=40, fill_padding=True,
                                        bgcolor = "white", use_backbuffer=False)
        inner_cont = VPlotContainer(padding=0, use_backbuffer=True)
        inner_cont.add(self.horiz_cross_plot)
        inner_cont.add(self.color_plot)
        self.container.add(self.colorbar)
        self.container.add(inner_cont)
        self.container.add(self.vert_cross_plot)
        
    def _metadata_changed(self, old, new):
        """ This function takes out a cross section from the image data, based
        on the line inspector selections, and updates the line and scatter
        plots."""

        #self.cross_plot.value_range.low = self.minz
        #self.cross_plot.value_range.high = self.maxz
        #self.cross_plot2.value_range.low = self.minz
        #self.cross_plot2.value_range.high = self.maxz
        if self._imag_index.metadata.has_key("selections"):
            x_ndx, y_ndx = self._imag_index.metadata["selections"]
            if y_ndx and x_ndx:
#                xdata, ydata = self._image_index.get_data()
#                xdata, ydata = xdata.get_data(), ydata.get_data()
                self.pd_horiz.set_data("horiz", self._image_value.data[y_ndx,:])
                self.pd_vert.set_data("vert", self._image_value.data[:,x_ndx])
#                    scatter_index=array([xdata[x_ndx]]),
#                    scatter_index2=array([ydata[y_ndx]]),
#                    scatter_value=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_value2=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_color=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_color2=array([self._image_value.data[y_ndx, x_ndx]])
#                )
#        else:
#            self.pd.update_data({"scatter_value": array([]),
#                "scatter_value2": array([]), "line_value": array([]),
#                "line_value2": array([])})

#if __name__ == "__main__":

#    filename="/Users/thomasaref/Dropbox/Dad stuff/sample3/digitizer/lt/sample3_digitizer_f_sweep_t_300mk_100nspulse.hdf5"
#    
#    with h5py.File(filename, 'r') as f:
#        
#        time=f["Traces"]["d - AvgTrace - t"][:]
#        Magvec=f["Traces"]["d - AvgTrace - Magvec"][:]
#        frequency=f["Data"]["Data"][:]
#    #    for name in f["Data"]:
#    #        print name
#        
#    time=squeeze(time)
#    Magvec=squeeze(Magvec)
#    frequency=squeeze(frequency)
#
#    x = time[:,0]*1.0e6
#    y = frequency[0,:]/1.0e9
#    z=transpose(Magvec*1000.0)
#    
#    ip=myImagePlot(x,y,z)
#    ip.configure_traits()     
        